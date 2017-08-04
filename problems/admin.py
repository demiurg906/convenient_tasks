from django.contrib import admin
from django.db import IntegrityError
from tagging.models import Tag

from problems.models import Task, User, TaskSource, Section, Subsection, Image, Grade, TaskTip, TaskCondition, TaskAnswer, TaskSolution


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ('image_tag', 'number', 'section')
    readonly_fields = ('image_tag',)


@admin.register(TaskAnswer, TaskCondition, TaskTip, TaskSolution)
class TaskSectionAdmin(admin.ModelAdmin):
    fields = ('text', )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ('condition', 'tip', 'solution', 'answer', 'tags', 'section', 'subsection', 'grades', 'source')
    list_display = ('task_name', 'has_tip', 'has_solution', 'has_answer', 'section', 'subsection')

admin.site.register([User, TaskSource, Section, Subsection, Grade])
