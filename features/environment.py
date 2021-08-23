from fixtures import *

from behave import use_fixture
from behave.fixture import use_fixture_by_tag


def before_tag(context, tag):
    if tag.startswith('fixture.'):
        return use_fixture_by_tag(tag[8:], context, fixtures_registry)


def before_all(context):
    use_fixture(api_clients, context)
    use_fixture(random_seed, context)


def before_scenario(context, scenario):
    use_fixture(clear_environment, context)
