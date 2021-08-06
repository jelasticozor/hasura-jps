from fixtures import *

from behave import use_fixture
from behave.fixture import use_fixture_by_tag


def before_tag(context, tag):
    if tag.startswith('fixture.'):
        return use_fixture_by_tag(tag[8:], context, fixtures_registry)


def before_all(context):
    # the api client can be injected here because it is stateless
    # use_fixture(api_client, context)
    # use_fixture(random_seed, context)
    pass


def before_scenario(context, scenario):
    pass
