from django.core.management.base import BaseCommand, CommandError
from apps.common.models import Organization, Offer
from apps.worksheets.models import Worksheet


class Command(BaseCommand):
    help = """\
        Generate fake data, by default it generate for
        models: [organization, offer, worksheet]
    """
    model = {
        'organization': Organization,
        'offer': Offer,
        'worksheet': Worksheet,
    }
    default_count = {
        'organization': 500,
        'offer': 10000,
        'worksheet': 100000,
    }

    def add_arguments(self, parser):
        parser.add_argument(
            'model', nargs='?', type=str, default='',
            help='model name from list: organization, offer worksheet'
        )
        parser.add_argument(
            '-c', '--count', action='store', dest='count', type=int,
            default=None,
            help='count rows of data, default is default value for model'
        )
        parser.add_argument(
            '-l', '--locale', action='store', dest='locale', default='ru',
            help='localization setting for generating data, default is "ru"'
        )

    def handle(self, *args, **options):
        model_name = options['model']
        if not model_name:
            models_list = ['organization', 'offer', 'worksheet']
        else:
            models_list = [model_name.lower()]
        for _name in models_list:
            if _name not in self.model:
                continue
            model = self.model[_name]
            count = options['count']
            if not count:
                count = self.default_count[_name]
            try:
                model._bootstrap(count=count, locale=options['locale'])
            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR('Raised exception for "%s"' % _name)
                )
                self.stderr.write(exc)
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully generated data for "%s"' % _name
                    )
                )
