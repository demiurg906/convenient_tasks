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
    type = models.CharField(max_length=32)

    def get_parent(self):
        if self.type == 'condition':
            return self.condition
        if self.type == 'tip':
            return self.tip
        if self.type == 'solution':
            return self.solution
        if self.type == 'answer':
            return self.answer
        raise RuntimeError(f'Неверный тип части задачи -- {self.type}')

    def __str__(self):
        return f'{self.type} for {self.get_parent()}'


class Task(models.Model):
    """
    Модель для задачи
    """
    condition = models.OneToOneField(TaskSection, related_name='condition')  # условие
    tip = models.OneToOneField(TaskSection, related_name='tip', null=True)  # подсказка
    solution = models.OneToOneField(TaskSection, related_name='solution', null=True)  # решение
    answer = models.OneToOneField(TaskSection, related_name='answer', null=True)  # ответ

    tags = TagField()

    section = models.ForeignKey(Section, related_name='section')  # основной раздел (физика/математика)
    subsection = models.ForeignKey(Subsection, related_name='subsection')  # подраздел

    grades = models.ManyToManyField(Grade, blank=True)  # классы для данной задачи

    source = models.OneToOneField(TaskSource, null=True)  # источник задачи

    def __str__(self):
        return f'Задача {str(self.pk)}'


class Image(models.Model):
    """
    Модель для иллюстрации к части задачи
    """
    image = models.ImageField(null=True)  # сама картинка
    number = models.IntegerField()  # ее номер в задаче
    tex_src = models.TextField(null=True)  # TeX представление картинки
    section = models.ForeignKey(TaskSection, on_delete=models.CASCADE)  # ссылка на задачу

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="{self.image.width}" height="{self.image.height}" />')

    image_tag.short_description = 'Image'

    def __str__(self):
        return f'image {self.number} for {self.section}'
