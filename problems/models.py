import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe
from tagging.fields import TagField
from tagging.models import Tag


class User(AbstractUser):
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if not self.taskpool_set.filter(name='Избранное').exists():
            TaskPool.objects.create(
                name='Избранное',
                user=self
            )
        dir_name = os.path.join(settings.TEMPORARY_FOLDER, settings.USERS_FILES, str(self.username))
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)


class GradeManager(models.Manager):
    def range(self, min_grade=1, max_grade=11):
        return self.filter(grade__gte=min_grade).filter(grade__lte=max_grade).all()


class Grade(models.Model):
    """
    Модель для класса
    """
    PATTERN = '{} класс'

    grade = models.SmallIntegerField(unique=True, verbose_name='Класс')
    tag = models.OneToOneField(Tag, on_delete=models.CASCADE)

    objects = GradeManager()

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
    tag = models.OneToOneField(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Section(AbstractSection):
    pass


class Subsection(AbstractSection):
    main_section = models.ForeignKey(Section, on_delete=models.CASCADE)


class Task(models.Model):
    """
    Модель для задачи
    """
    tags = TagField(verbose_name='Теги')

    section = models.ForeignKey(Section, related_name='section', verbose_name='Раздел', on_delete=models.CASCADE)  # основной раздел
    subsection = models.ForeignKey(Subsection, related_name='subsection', verbose_name='Подраздел', on_delete=models.CASCADE)  # подраздел

    grades = models.ManyToManyField(Grade, blank=True, verbose_name='Классы')  # классы для данной задачи

    tex_used = models.BooleanField(default=False, verbose_name='TeX')

    def __str__(self):
        return f'Задача {str(self.pk)}'

    def name(self):
        return str(self)

    name.short_description = 'Task name'
    name.admin_order_field = 'pk'

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
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE)  # ссылка на автора
    source = models.OneToOneField(Task, on_delete=models.CASCADE)  # ссылка на задачу

    def __str__(self):
        return f'Источник для "{self.source}"'


class TaskPool(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(default='')
    tasks = models.ManyToManyField(Task)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'"{self.name}" of user {self.user}'
