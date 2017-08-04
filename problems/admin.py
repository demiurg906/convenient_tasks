import nested_inline.admin

from django.contrib import admin

from problems.models import Task, User, TaskSource, Section, Subsection, Image, Grade, TaskTip, TaskCondition, TaskAnswer, TaskSolution


# INLINE_CLASS = admin.TabularInline
INLINE_CLASS = nested_inline.admin.NestedTabularInline


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ('image_tag', 'number', 'section')
    readonly_fields = ('image_tag',)


class ImageInline(nested_inline.admin.NestedStackedInline):
    model = Image
    extra = 0
    fields = ('image_tag', )
    readonly_fields = ('image_tag',)


@admin.register(TaskAnswer, TaskCondition, TaskTip, TaskSolution)
class TaskSectionAdmin(admin.ModelAdmin):
    fields = ('text', )
    inlines = (ImageInline, )


class TaskConditionInline(INLINE_CLASS):
    model = TaskCondition
    inlines = (ImageInline, )


class TaskTipInline(INLINE_CLASS):
    model = TaskTip
    inlines = (ImageInline, )


class TaskSolutionInline(INLINE_CLASS):
    model = TaskSolution
    inlines = (ImageInline, )


class TaskAnswerInline(INLINE_CLASS):
    model = TaskAnswer
    inlines = (ImageInline, )


@admin.register(Task)
class TaskAdmin(nested_inline.admin.NestedModelAdmin):
    fields = ('tags', 'section', 'subsection', 'grades', 'source')
    list_display = ('task_name', 'tex_used', 'has_tip', 'has_solution', 'has_answer', 'section', 'subsection')
    inlines = (TaskConditionInline, TaskTipInline, TaskSolutionInline, TaskAnswerInline)

admin.site.register([User, TaskSource, Section, Subsection, Grade])
