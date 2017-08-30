import nested_inline.admin

from django.contrib import admin
from django.db import models

from problems.forms import EditableTexTextarea
from problems.models import Task, User, TaskSource, Section, Subsection, Image, Grade, TaskSection, TaskPool


class TaskSourceInline(nested_inline.admin.NestedStackedInline):
    model = TaskSource
    readonly_fields = ('author', )


class ImageInline(nested_inline.admin.NestedStackedInline):
    model = Image
    extra = 0
    fields = ('image_tag', )
    readonly_fields = ('image_tag',)


class TaskSectionInline(nested_inline.admin.NestedStackedInline):
    model = TaskSection
    extra = 0
    max_num = 4
    inlines = (ImageInline, )
    formfield_overrides = {
        models.TextField: {'widget': EditableTexTextarea},
    }


def custom_titled_filter(title):
    """
    функция для list_filter для переопределния заголовка сортировки
    """
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


@admin.register(Task)
class TaskAdmin(nested_inline.admin.NestedModelAdmin):
    list_display = ('name', 'tex_used', 'has_tip', 'has_solution', 'has_answer', 'section', 'subsection')
    list_filter = ('tex_used',
                   ('section__name', custom_titled_filter('Section')),
                   ('subsection__name', custom_titled_filter('Subsection'))
                   )

    fields = ('tags', 'section', 'subsection', 'grades', 'tex_used')
    inlines = (TaskSourceInline, TaskSectionInline)
    # save_on_top = True  # useless with django-bootstrap

admin.site.register([User, Section, Subsection, Grade, TaskPool])
