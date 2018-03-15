from pytz import utc
import uuid
from random import randint, choice
from mimesis import Text, Datetime, Business, Person
from mimesis.builtins import RussiaSpecProvider
from mimesis.enums import Gender
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Model
from django.db import connection, transaction
from apps.common.models import Organization, Offer
from apps.worksheets.models import Worksheet


def _generate_offer_data(locale='ru') -> dict:
    text = Text(locale)
    datetime = Datetime(locale)
    typ_choice = [Offer.CONSUMER, Offer.MORTGAGE, Offer.AUTO, Offer.CSMB]
    created = datetime.datetime(start=2015, end=2017)
    _score = randint(0, 1000)

    def rand_dt():
        _dt = datetime.datetime(start=2017, end=2018)
        return _dt.replace(tzinfo=utc)

    return dict(id=uuid.uuid4(),
                created=created.replace(tzinfo=utc),
                updated=created.replace(tzinfo=utc),
                rotation_start=rand_dt(),
                rotation_finish=rand_dt(),
                name=' '.join(text.words(quantity=10)),
                typ=choice(typ_choice),
                min_score=_score,
                max_score=_score + randint(300, 1000))


def _generate_organization_data(locale='ru') -> dict:
    business = Business(locale)
    return dict(id=uuid.uuid4(), name=business.company())


def _generate_worksheet_data(locale='ru') -> dict:
    person = Person(locale)
    rus_spec = RussiaSpecProvider()
    datetime = Datetime(locale)
    g = choice([Gender.FEMALE, Gender.MALE])
    created = datetime.datetime(start=2015, end=2018)
    return dict(created=created.replace(tzinfo=utc),
                updated=created.replace(tzinfo=utc),
                surname=person.surname(gender=g),
                first_name=person.name(gender=g),
                patronymic=rus_spec.patronymic(gender=g),
                birth_date=datetime.datetime(start=1960, end=1998).date(),
                phone_num=person.telephone(),
                pass_ser=rus_spec.passport_series(),
                pass_num=rus_spec.passport_number(),
                score=randint(0, 2000))


@transaction.atomic
def insert(tab_name: str, data_dict: dict):
    values, fields, places = [], [], []
    for key, val in data_dict.items():
        fields.append(key)
        places.append('%s')
        values.append(val)
    sql = "INSERT INTO {tab_name} ({fields}) VALUES ({places})"\
        .format(tab_name=tab_name,
                fields=', '.join(fields),
                places=', '.join(places))
    with connection.cursor() as cursor:
        cursor.execute(sql, values)


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
    generate_data = {
        'organization': _generate_organization_data,
        'offer': _generate_offer_data,
    }
    default_count = {
        'organization': 100,
        'offer': 1000,
        'worksheet': 10000,
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
            count = options['count']
            if not count:
                count = self.default_count[_name]
            try:
                self._fill_data(_name, count, options['locale'])
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

    def _fill_data(self, model_name, count, locale='ru'):
        ModelKlass: type(Model) = self.model[model_name]
        ModelKlass.objects.all().delete()
        db_table = ModelKlass._meta.db_table
        organizations_id = []
        if model_name == 'offer':
            organizations_id = Organization.objects.values_list('pk', flat=True)
        for _ in range(count):
            _data = self.generate_data[model_name](locale)
            if model_name == 'offer':
                _data['organization_id'] = choice(organizations_id)
            insert(db_table, _data)
