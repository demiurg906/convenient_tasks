from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models, IntegrityError
from django.utils.safestring import mark_safe
from tagging.fields import TagField
from tagging.models import Tag
from tagging.registry import register


class User(AbstractUser):
    pass


class Grade(models.Model):
    """
    Модель для класса
    """
    PATTERN = '{} класс'

    grade = models.IntegerField(
        unique=True,
    )

    tag = models.OneToOneField(Tag)

    def __str__(self):
        return str(self.PATTERN.format(self.grade))


class TaskSource(models.Model):
    name = models.CharField(max_length=100)  # название источника
    url = models.URLField(null=True)  # ссылка на источник
    author = models.OneToOneField(settings.AUTH_USER_MODEL, null=True)  # ссылка на автора

    def __str__(self):
        return f'source for {self.task}'


class AbstractSection(models.Model):
    """
    Модель раздела задач
    (как основного раздела (физика/математика)), так и побочных
    """
    name = models.CharField(max_length=100, unique=True)
    tag = models.OneToOneField(Tag)

    def __str__(self):
        return self.name


class Section(AbstractSection):
    pass


class Subsection(AbstractSection):
    pass


class TaskSection(models.Model):
    """
    Модель для части задачи -- условия, подсказки, решения или ответа
    содержит в себе текст и 0 или больше картинок
    """
    text = models.TextField(default='')


class TaskCondition(TaskSection):
    def __str__(self):
        return f'condition for {self.condition}'


class TaskTip(TaskSection):
    def __str__(self):
        return f'tip for {self.tip}'


class TaskSolution(TaskSection):
    def __str__(self):
        return f'solution for {self.solution}'


class TaskAnswer(TaskSection):
    def __str__(self):
        return f'answer for {self.answer}'


class Task(models.Model):
    """
    Модель для задачи
    """
    condition = models.OneToOneField(TaskCondition, related_name='condition')  # условие
    tip = models.OneToOneField(TaskTip, related_name='tip', null=True)  # подсказка
    solution = models.OneToOneField(TaskSolution, related_name='solution', null=True)  # решение
    answer = models.OneToOneField(TaskAnswer, related_name='answer', null=True)  # ответ

    tags = TagField()

    section = models.ForeignKey(Section, related_name='section')  # основной раздел (физика/математика)
    subsection = models.ForeignKey(Subsection, related_name='subsection')  # подраздел

    grades = models.ManyToManyField(Grade, blank=True)  # классы для данной задачи

    source = models.OneToOneField(TaskSource, null=True)  # источник задачи

    def __str__(self):
        return f'Задача {str(self.pk)}'

    def task_name(self):
        return str(self)

    task_name.short_description = 'Task name'
    task_name.admin_order_field = 'pk'


class Image(models.Model):
    """
    Модель для иллюстрации к части задачи
    """
    image = models.ImageField(null=True)  # сама картинка
    number = models.IntegerField()  # ее номер в задаче
    section = models.ForeignKey(TaskSection, on_delete=models.CASCADE)  # ссылка на задачу

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="{self.image.width}" height="{self.image.height}" />')

    image_tag.short_description = 'Image'

    def __str__(self):
        return f'image {self.number} for {self.section}'
