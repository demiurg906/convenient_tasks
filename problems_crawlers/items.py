# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from problems.models import Grade, TaskSource, Section, Subsection, Image, Task, TaskSection
from scrapy_djangoitem import DjangoItem


class GradeItem(DjangoItem):
    django_model = Grade


class TaskSourceItem(DjangoItem):
    django_model = TaskSource


class SectionItem(DjangoItem):
    django_model = Section


class SubsectionItem(DjangoItem):
    django_model = Subsection


class TaskSectionItem(DjangoItem):
    django_model = TaskSection


TASK_SECTIONS = {
    'condition': TaskSection.CONDITION,
    'tip': TaskSection.TIP,
    'solution': TaskSection.SOLUTION,
    'answer': TaskSection.ANSWER
}


class ImageItem(DjangoItem):
    django_model = Image


class TaskItem(DjangoItem):
    django_model = Task


class ParseResultItem(scrapy.Item):
    source = scrapy.Field()
    themes = scrapy.Field()
    grades = scrapy.Field()
    # task -- словарь, содержащий в себе информацию о задаче в следующем виде:
    # ключ -- имя секции, значение -- пара (text, pictures),
    # где images -- список кортежей вида (image_url, tex_view)
    task = scrapy.Field()
    section = scrapy.Field()
    subsection = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    tex_used = scrapy.Field()
