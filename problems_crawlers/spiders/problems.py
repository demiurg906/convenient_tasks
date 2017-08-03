from functools import partial
from urllib.parse import urlparse, parse_qs, urlsplit, urlencode, urlunsplit
from problems_crawlers.items import GradeItem, TaskSectionItem, TaskSourceItem, SectionItem, ImageItem, TaskItem, \
    ParseResultItem

import scrapy
import re

from scrapy.http.response.html import HtmlResponse

DEFAULT_SECTIONS = ['Условие', 'Подсказка', 'Решение', 'Ответ']

CONTENT_PATTERN = re.compile(r'Условие|Подсказка|Решение|Ответ|Источники и прецеденты использования')

DEFAULT_NAMES = {'Условие': 'condition', 'Подсказка': 'tip', 'Решение': 'solution', 'Ответ': 'answer', }
"""
Данный паук предназначен для сайта problems.ru
"""


MAX_TASK_NUMBER = 130000
# MAX_TASK_NUMBER = 10
START_TASK_NUMBER = 1
TABLE_OF_CONTEXT_URL = 'http://problems.ru/view_by_subject_new.php?parent=1302'
# задача с картинкой
# SINGLE_TASK_URL = 'http://problems.ru/view_problem_details_new.php?id=104117'
# задача с двумя подтемами
# SINGLE_TASK_URL = 'http://problems.ru/view_problem_details_new.php?id=65330'
# задача с двумя TeX версткой
SINGLE_TASK_URL = 'http://problems.ru/view_problem_details_new.php?id=102718'
GET_PARAMETER_TEMPLATE = '&start='

SECTION = 'Математика'


class ProblemsSpider(scrapy.Spider):
    name = 'problems'

    def start_requests(self):
        start_url = getattr(self, 'start_url', None)

        # if start_url is None:
        #     start_url = TABLE_OF_CONTEXT_URL + str(START_TASK_NUMBER)
        # yield scrapy.Request(url=start_url, callback=self.parse_table_of_context)

        if start_url is None:
            start_url = SINGLE_TASK_URL
        yield scrapy.Request(url=start_url, callback=self.parse_task)

    def parse_table_of_context(self, response: HtmlResponse):
        ul = response.css('ul.componentboxlist')
        themes = {text.strip(): [url, 0] for text, url in zip(ul.css('a::text').extract(), ul.css('a::attr(href)').extract())}
        titles = ul[0].css('::text').extract()
        for i, s in enumerate(titles):
            s = s.strip()
            if s in themes:
                s_n = titles[i + 1]
                n = int(s_n.strip().split()[0][1:])
                themes[s][1] = n

        for subsection, (url, n) in themes.items():
            url = set_get_parameter(response.urljoin(url), 'start', 0)
            callback = partial(self.parse_list_of_tasks, max_number=n, next_number=5, subsection=subsection)
            yield response.follow(url, callback=callback)

    def parse_list_of_tasks(self, response: HtmlResponse, max_number=0, next_number=0, step=5, subsection:str = ''):
        task_urls = response.css('.problemsmallnumber .componentboxlink::attr(href)').extract()
        for task_url in task_urls:
            callback = partial(self.parse_task, subsection=subsection)
            yield response.follow(response.urljoin(task_url), callback=callback)
        if next_number < max_number:
            url = set_get_parameter(response.url, 'start', next_number)
            callback = partial(self.parse_list_of_tasks, max_number=max_number, next_number=next_number + step, subsection=subsection)
            yield response.follow(url, callback=callback)

    # TODO: убрать empty
    def parse_task(self, response: HtmlResponse, subsection='empty'):
        # Source
        task_name = response.css('table.viewingtable div.componentboxheader::text').extract_first().strip()
        source = TaskSourceItem()
        source['name'] = task_name
        source['url'] = response.url

        content = response.css('table.viewingtable .componentboxcontents')

        # Themes
        info = content.css('table.problemdetailscaptiontable')
        themes = [theme.strip() for theme in info.css('.problemdetailssubject .problemdetailssubjecttablecell a.componentboxlink::text').extract()]

        # Grades
        _, grades = info.css('.problemdetailsdifficulty nobr::text').extract()
        grades = list(map(lambda n: int(n), re.findall(r'\d+', grades)))

        # Task
        task_dict, image_urls = self.extract_task(content, response)

        yield ParseResultItem(
            source=source,
            themes=themes,
            grades=grades,
            task=task_dict,
            section=SECTION,
            subsection=subsection,
            image_urls=image_urls
        )

    def extract_task(self, content: scrapy.Selector, response: HtmlResponse):
        """
        Вытаскивает информацию о задаче из содержимого страницы
        :return: словарь с ключами по именам секций задачи и со значениями вида
                 text, images, где images -- список кортежей вида (image_url, tex_view)
        """
        # Вытаскивание текста
        text = ' '.join(''.join(content.css('::text').extract()).split())
        sections = CONTENT_PATTERN.findall(text)
        parts = list(map(lambda s: s.strip(), CONTENT_PATTERN.split(text)))
        names = {section: sections.index(section) + 1 for section in DEFAULT_SECTIONS if section in sections}
        task_dict = {DEFAULT_NAMES[section]: (parts[i], []) for section, i in names.items()}

        # вытаскивание картинок
        def check_h3(s: str):
            for section in DEFAULT_NAMES:
                if s.startswith('h3') and section in s:
                    return DEFAULT_NAMES[section]
            return False

        section = None
        image_urls = []
        for line in content.extract_first().split('<'):
            title = check_h3(line)
            if title:
                section = title
                continue
            if section and line.startswith('img'):
                src = re.search(r'src=\".+\d+\"', line).group()
                if src:
                    tex = re.search(r'alt=\"\$(.|\n)+\$\"', line).group()
                    tex_src = ''
                    if tex:
                        tex_src = tex[5:-1]
                        image_src = ''
                    else:
                        image_src = src[5:-1]
                        image_url = response.urljoin(image_src)
                        image_urls.append(image_url)
                    task_dict[section][1].append((image_url, tex_src))
        return task_dict, image_urls


def set_get_parameter(url, name, value):
    """
    Устанавливает в url Get параметр
    :return str: готовый URL
    """
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    params = parse_qs(query_string)
    params[name] = [value]
    new_query_string = urlencode(params, doseq=True)
    return urlunsplit((scheme, netloc, path, new_query_string, fragment))
