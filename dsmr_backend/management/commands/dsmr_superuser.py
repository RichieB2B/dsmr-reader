from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from decouple import config


class Command(BaseCommand):  # noqa
    help = 'Persists or updates a superuser, as defined by the environment vars.'

    def handle(self, **options):
        """ WARNING: Only safe for command line execution. Do NOT use for web requests! """
        username = config(
            'DSMR_USER',  # @deprecated v4.5, removed v5.0
            default=config('DSMRREADER_ADMIN_USER', default=None)
        )
        password = config(
            'DSMR_PASSWORD',  # @deprecated v4.5, removed v5.0
            default=config('DSMRREADER_ADMIN_PASSWORD')
        )

        if not username or not password:
            raise CommandError(
                'Either DSMRREADER_ADMIN_USER or DSMRREADER_ADMIN_PASSWORD (or both) are missing/empty in (.)env'
            )

        try:
            user = User.objects.get(
                username=username,
                is_superuser=True
            )
        except User.DoesNotExist:
            print('Creating new superuser "{}"'.format(username))
            User.objects.create_superuser(username, '{}@localhost'.format(username), password)
        else:
            print('Updating password of superuser "{}"'.format(username))
            user.set_password(password)
            user.save()
