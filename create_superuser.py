import os
import django
from django.conf import settings



if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'convenient_tasks.settings'
    # settings.configure()
    django.setup()
    from django.db import IntegrityError
    from problems.models import User
    try:
        User.objects.create_superuser(username='admin', password='qwerty123', email='')
    except IntegrityError:
        pass
