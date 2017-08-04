# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from django.db import IntegrityError
from tagging.models import Tag

from problems.models import Section, Grade, Subsection
from problems_crawlers.items import GradeItem, SectionItem, ImageItem, TaskItem, \
    ParseResultItem, SubsectionItem, TASK_SECTIONS


class CheckConditionPipeline:
    def process_item(self, item: ParseResultItem, spider):
        if 'condition' not in item['task']:
            return {
                'error': f'{item["task"]["source"]}'
            }
        return item


class ProblemsCrawlersPipeline(object):
    def process_item(self, item: ParseResultItem, spider):
        if 'error' in item:
            return item

        image_dict = {}
        for image in item['images']:
            image_dict[image['url']] = os.path.normpath(image['path'])

        source = item['source'].save()
        section = self.save_unique_item(Section, SectionItem, 'name', item['section'], True)
        subsection = self.save_unique_item(Subsection, SubsectionItem, 'name', item['subsection'], True)

        task = TaskItem()
        task['section'] = section
        task['subsection'] = subsection

        for field, (text, pictures) in item['task'].items():
            task_section = TASK_SECTIONS[field]()
            task_section['text'] = text
            task_section = task_section.save()
            for n, image_url in enumerate(pictures):
                image = ImageItem()
                image['section'] = task_section
                image['image'] = image_dict[image_url]
                image['number'] = n + 1
                image.save()
            task[field] = task_section
        task['source'] = source
        task = task.save()
        tags = set()

        def add_tag(item):
            tags.add(f'\"{str(item.tag)}\"')

        add_tag(section)
        add_tag(subsection)

        for theme in item['themes']:
            tags.add(f'\"{theme}\"')

        grades = [self.save_unique_item(Grade, GradeItem, 'grade', grade, True, '{} класс') for grade in item['grades']]
        for grade in grades:
            task.grades.add(grade)
            add_tag(grade)

        task.tags = ' '.join(tags)
        task.save()
        print()
        return {
            'task': task.pk
        }

    def save_unique_item(self, model_class, item_class, field, value, tag=False, tag_pattern='{}'):
        item = item_class()
        item[field] = value
        if tag:
            tag, _ = Tag.objects.get_or_create(name=tag_pattern.format(value))
            item['tag'] = tag
        try:
            return item.save()
        except IntegrityError as e:
            return model_class.objects.get(**{field: value})
