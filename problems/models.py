from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models, IntegrityError
from django.utils.safestring import mark_safe
from tagging.fields import TagField
from tagging.models import Tag


class User(AbstractUser):
    pass


class Grade(models.Model):
    """
    Модель для класса
    """
    PATTERN = '{} класс'

    grade = models.SmallIntegerField(unique=True, verbose_name='Класс')

    tag = models.OneToOneField(Tag)

    def __str__(self):
        return str(self.PATTERN.format(self.grade))

    class Meta:
        ordering = ['grade']


class AbstractSection(models.Model):
    """
    Модель раздела задач
    (как основного раздела (физика/математика)), так и побочных
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    tag = models.OneToOneField(Tag)

    def __str__(self):
        return self.name


class Section(AbstractSection):
    pass


class Subsection(AbstractSection):
    pass


class Task(models.Model):
    """
    Модель для задачи
    """
    tags = TagField(verbose_name='Теги')

    section = models.ForeignKey(Section, related_name='section', verbose_name='Раздел')  # основной раздел (физика/математика)
    subsection = models.ForeignKey(Subsection, related_name='subsection', verbose_name='Подраздел')  # подраздел

    grades = models.ManyToManyField(Grade, blank=True, verbose_name='Классы')  # классы для данной задачи

    tex_used = models.BooleanField(default=False, verbose_name='TeX')

    def __str__(self):
        return f'Задача {str(self.pk)}'

    def task_name(self):
        return str(self)

    task_name.short_description = 'Task name'
    task_name.admin_order_field = 'pk'

    def has_tip(self):
        return any(section.is_tip for section in self.tasksection_set.all())

    has_tip.boolean = True
    has_tip.short_description = 'Tip'

    def has_solution(self):
        return any(section.is_solution for section in self.tasksection_set.all())

    has_solution.boolean = True
    has_solution.short_description = 'Solution'

    def has_answer(self):
        return any(section.is_answer for section in self.tasksection_set.all())

    has_answer.boolean = True
    has_answer.short_description = 'Answer'


class TaskSection(models.Model):
    """
    Модель для части задачи -- условия, подсказки, решения или ответа
    содержит в себе текст и 0 или больше картинок
    """
    CONDITION = '1'
    TIP = '2'
    SOLUTION = '3'
    ANSWER = '4'

    TYPOS = {
        CONDITION: 'Условие',
        TIP: 'Подсказка',
        SOLUTION: 'Решение',
        ANSWER: 'Ответ'
    }

    text = models.TextField(default='', verbose_name='Текст')
    type = models.CharField(max_length=1, choices=TYPOS.items(), verbose_name='Тип')
    task = models.ForeignKey(Task)

    def __str__(self):
        return f'{self.TYPOS[self.type]} для "{self.task}"'

    def is_condition(self):
        return self.type == self.CONDITION

    def is_tip(self):
        return self.type == self.TIP

    def is_solution(self):
        return self.type == self.SOLUTION

    def is_answer(self):
        return self.type == self.ANSWER

    def get_name(self):
        return self.TYPOS[self.type]


class Image(models.Model):
    """
    Модель для иллюстрации к части задачи
    """
    image = models.ImageField(null=True)  # сама картинка
    number = models.IntegerField(verbose_name='Номер')  # ее номер в задаче
    section = models.ForeignKey(TaskSection, on_delete=models.CASCADE)  # ссылка на задачу

    def image_tag(self):
        return mark_safe(f'<img {self.tag_params()} '
                         f'alt="рис. {self.number}"/>')

    def tag_params(self):
        return f'src={self.image.url} width={self.image.width} height={self.image.height}'

    image_tag.short_description = 'Image'

    def __str__(self):
        return f'Рис. {self.number} of "{self.section}"'


class TaskSource(models.Model):
    name = models.CharField(max_length=100, null=True, verbose_name='Имя')  # название источника
    url = models.URLField(null=True)  # ссылка на источник
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор')  # ссылка на автора
    source = models.OneToOneField(Task)  # ссылка на задачу

    def __str__(self):
        return f'Источник для "{self.source}"'
