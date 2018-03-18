from pytz import utc
import uuid
from itertools import chain
from string import ascii_letters, digits
from random import randint, choice
from mimesis import Text, Datetime, Business, Person
from mimesis.builtins import RussiaSpecProvider
from mimesis.enums import Gender
from mimesis.helpers import get_random_item
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Model
from django.db import connection, transaction
from django.contrib.auth.models import User, Group
from apps.common.models import Organization, Offer
from apps.common.constants import GROUP_PARTNERS, GROUP_CREDITS
from apps.questionnaires.models import Questionnaire


def _generate_offer_data(locale='ru') -> dict:
    text = Text(locale)
    datetime = Datetime(locale)
    typ_choice = [Offer.CONSUMER, Offer.MORTGAGE, Offer.AUTO, Offer.CSMB]
    created = datetime.datetime(start=2015, end=2017)
    _score = randint(0, 1000)

    def rand_dt():
        _dt = datetime.datetime(start=2017, end=2018)
        return _dt.replace(tzinfo=utc)

    return {
        'id': uuid.uuid4(),
        'created': created.replace(tzinfo=utc),
        'updated': created.replace(tzinfo=utc),
        'rotation_start': rand_dt(),
        'rotation_finish': rand_dt(),
        'name': ' '.join(text.words(quantity=10)),
        'typ': choice(typ_choice),
        'min_score': _score,
        'max_score': _score + randint(300, 1000),
    }


def _generate_organization_data(locale='ru') -> dict:
    business = Business(locale)
    return {
        'id': uuid.uuid4(),
        'name': business.company(),
    }


def _generate_questionnaire_data(locale='ru') -> dict:
    person = Person(locale)
    rus_spec = RussiaSpecProvider()
    datetime = Datetime(locale)
    g = get_random_item(Gender)
    created = datetime.datetime(start=2015, end=2018)
    return {
        'id': uuid.uuid4(),
        'created': created.replace(tzinfo=utc),
        'updated': created.replace(tzinfo=utc),
        'surname': person.surname(gender=g),
        'first_name': person.name(gender=g),
        'patronymic': rus_spec.patronymic(gender=g),
        'birth_date': datetime.datetime(start=1960, end=1998).date(),
        'phone_num': person.telephone(),
        'pass_ser': rus_spec.passport_series(),
        'pass_num': rus_spec.passport_number(),
        'score': randint(0, 2000),
    }


def _generate_password(length: int = 10) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))


def _generate_user_data(locale='ru'):
    person = Person(locale)
    date = Datetime(locale)
    gender = get_random_item(Gender)
    return {
        'password': _generate_password(),
        'first_name': person.surname(gender=gender),
        'last_name': person.name(gender=gender),
        'email': person.email(),
        'date_joined': date.datetime(start=2014, end=2015).replace(tzinfo=utc),
    }


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


class NoDataException(Exception):
    pass


class Command(BaseCommand):
    help = """\
        Generate fake data, by default it generate for
        models: [organization, offer, questionnaire]
    """
    model = {
        'user': User,
        'organization': Organization,
        'offer': Offer,
        'questionnaire': Questionnaire,
    }
    ORGANIZATION = 'organization'
    OFFER = 'offer'
    QUESTIONNAIRE = 'questionnaire'
    USER = 'user'
    APPLICATION = 'claim'
    generate_data = {
        ORGANIZATION: _generate_organization_data,
        OFFER: _generate_offer_data,
        QUESTIONNAIRE: _generate_questionnaire_data,
        USER: _generate_user_data,
    }
    default_count = {
        ORGANIZATION: 50,
        OFFER: 400,
        QUESTIONNAIRE: 2000,
    }

    def add_arguments(self, parser):
        parser.add_argument(
            'model', nargs='?', type=str, default='',
            help='model name from list: organization, offer questionnaire'
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
            models_list = [self.USER,
                           self.ORGANIZATION,
                           self.OFFER,
                           self.QUESTIONNAIRE]
        else:
            models_list = [model_name.lower()]
        for _name in models_list:
            if _name not in self.model:
                continue
            count = options['count']
            if not count:
                count = self.default_count[_name if _name != self.USER
                                           else self.ORGANIZATION]
            try:
                if _name == self.USER:
                    users_1 = self._fill_users('partner{n:02d}', GROUP_PARTNERS,
                                               10, options['locale'])

                    users_2 = self._fill_users('credit{n:02d}', GROUP_CREDITS,
                                               count, options['locale'])
                    with open('fake_users.txt', 'w') as f:
                        f.writelines('{}:{}\n'.format(k, v)
                                     for k, v in chain(users_1.items(),
                                                       users_2.items()))
                else:
                    self._fill_data(_name, count, options['locale'])
            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR('Raised exception for "%s"' % _name)
                )
                self.stderr.write(str(exc))
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully generated data for "%s"' % _name
                    )
                )

    def _fill_users(self, username_patt, group_name, count, locale='ru'):
        generated_users = {}
        group = Group.objects.get(name=group_name)
        group.user_set.all().delete()
        for n in range(1, count+1):
            _data = self.generate_data['user'](locale)
            _username = username_patt.format(n=n)
            generated_users[_username] = _data['password']
            user = User.objects.create(username=_username, **_data)
            user.set_password(_data['password'])
            user.groups.add(group)
            user.save()
        return generated_users

    def _fill_data(self, model_name, count, locale='ru'):
        ModelKlass: type(Model) = self.model[model_name]
        ModelKlass.objects.all().delete()
        db_table = ModelKlass._meta.db_table
        organizations_id, users_id = [], []
        if model_name in (self.APPLICATION, self.QUESTIONNAIRE):
            users_id = list(User.objects
                            .filter(groups__name=GROUP_PARTNERS)
                            .values_list('pk', flat=True))
            if not users_id:
                raise NoDataException('Generate users first!')
        elif model_name == self.ORGANIZATION:
            users_id = list(User.objects
                            .filter(groups__name=GROUP_CREDITS)
                            .values_list('pk', flat=True))
            if not users_id:
                raise NoDataException('Generate users first!')
        if model_name == self.OFFER:
            organizations_id = Organization.objects.values_list('pk', flat=True)
        for _ in range(count):
            _data = self.generate_data[model_name](locale)
            if model_name == self.OFFER:
                _data['organization_id'] = choice(organizations_id)
            if model_name in (self.APPLICATION, self.QUESTIONNAIRE):
                _data['owner_id'] = choice(users_id)
            elif model_name == self.ORGANIZATION:
                _data['user_id'] = choice(users_id)
                users_id.remove(_data['user_id'])
            insert(db_table, _data)
