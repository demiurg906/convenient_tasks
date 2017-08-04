# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from problems.models import Grade, TaskSource, Section, Subsection, Image, Task, TaskAnswer, TaskSolution, TaskCondition, TaskTip
from scrapy_djangoitem import DjangoItem


class GradeItem(DjangoItem):
    django_model = Grade


class TaskSourceItem(DjangoItem):
    django_model = TaskSource


class SectionItem(DjangoItem):
    django_model = Section


class SubsectionItem(DjangoItem):
    django_model = Subsection


class TaskConditionItem(DjangoItem):
    django_model = TaskCondition


class TaskTipItem(DjangoItem):
    django_model = TaskTip


class TaskSolutionItem(DjangoItem):
    django_model = TaskSolution


class TaskAnswerItem(DjangoItem):
    django_model = TaskAnswer


TASK_SECTIONS = {
    'condition': TaskConditionItem,
    'tip': TaskTipItem,
    'solution': TaskSolutionItem,
    'answer': TaskAnswerItem
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
