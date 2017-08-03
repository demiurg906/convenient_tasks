from django.contrib import admin
from django.db import IntegrityError
from tagging.models import Tag

from problems.models import Task, User, TaskSource, Section, Subsection, Image, TaskSection, Grade


@admin.register(Image)
class MainAdmin(admin.ModelAdmin):
    fields = ('image_tag', 'number', 'tex_src', 'section')
    readonly_fields = ('image_tag',)


admin.site.register([Task, User, TaskSource, Section, Subsection, TaskSection, Grade])
