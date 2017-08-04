from django.contrib import admin

from problems.models import Task, User, TaskSource, Section, Subsection, Image, Grade, TaskTip, TaskCondition, TaskAnswer, TaskSolution


INLINE_CLASS = admin.TabularInline


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ('image_tag', 'number', 'section')
    readonly_fields = ('image_tag',)


@admin.register(TaskAnswer, TaskCondition, TaskTip, TaskSolution)
class TaskSectionAdmin(admin.ModelAdmin):
    fields = ('text', )


class TaskConditionInline(INLINE_CLASS):
    model = TaskCondition


class TaskTipInline(INLINE_CLASS):
    model = TaskTip


class TaskSolutionInline(INLINE_CLASS):
    model = TaskSolution


class TaskAnswerInline(INLINE_CLASS):
    model = TaskAnswer


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ('tags', 'section', 'subsection', 'grades', 'source')
    list_display = ('task_name', 'has_tip', 'has_solution', 'has_answer', 'section', 'subsection')
    inlines = (TaskConditionInline, TaskTipInline, TaskSolutionInline, TaskAnswerInline)

admin.site.register([User, TaskSource, Section, Subsection, Grade])
