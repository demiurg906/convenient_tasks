import nested_inline.admin

from django.contrib import admin
from django import forms
from django.db import models
from django.forms import TextInput, Textarea

# from problems.forms import TexTextInput
from problems.models import Task, User, TaskSource, Section, Subsection, Image, Grade, TaskTip, TaskCondition, \
    TaskAnswer, TaskSolution, TaskSection


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ('image_tag', 'number', 'section')
    readonly_fields = ('image_tag',)


class ImageInline(nested_inline.admin.NestedStackedInline):
    model = Image
    extra = 0
    fields = ('image_tag', )
    readonly_fields = ('image_tag',)


class TaskSectionInline(nested_inline.admin.NestedTabularInline):
    model = TaskSection
    inlines = (ImageInline, )
    # formfield_overrides = {
    #     models.TextField: {'widget': TexTextInput},
    # }


class TaskConditionInline(TaskSectionInline):
    model = TaskCondition


class TaskTipInline(TaskSectionInline):
    model = TaskTip


class TaskSolutionInline(TaskSectionInline):
    model = TaskSolution


class TaskAnswerInline(TaskSectionInline):
    model = TaskAnswer


@admin.register(Task)
class TaskAdmin(nested_inline.admin.NestedModelAdmin):
    fields = ('tags', 'section', 'subsection', 'grades', 'source', 'tex_used')
    list_display = ('task_name', 'tex_used', 'has_tip', 'has_solution', 'has_answer', 'section', 'subsection')
    inlines = (TaskConditionInline, TaskTipInline, TaskSolutionInline, TaskAnswerInline)

admin.site.register([User, TaskSource, Section, Subsection, Grade])
