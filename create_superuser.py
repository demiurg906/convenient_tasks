import os
import django


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'convenient_tasks.settings'
    django.setup()
    from django.db import IntegrityError
    from problems.models import User
    try:
        User.objects.create_superuser(username='admin', password='qwerty123', email='')
    except IntegrityError:
        pass
