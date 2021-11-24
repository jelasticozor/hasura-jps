from behave import use_fixture
from behave.fixture import use_fixture_by_tag

from fixtures import *


def before_tag(context, tag):
    if tag.startswith('fixture.'):
        return use_fixture_by_tag(tag[8:], context, fixtures_registry)


def before_all(context):
    use_fixture(random_seed, context)
    use_fixture(worker_id, context)
    use_fixture(commit_sha, context)
    use_fixture(project_root_folder, context)
    use_fixture(jelastic_clients_factory, context)
    use_fixture(fusionauth_admin_email, context)
    use_fixture(fusionauth_issuer, context)
    use_fixture(path_to_serverless_test_configuration, context)
    use_fixture(fusionauth_version, context)
    use_fixture(registered_user_role, context)
    use_fixture(jelastic_environment, context)
    use_fixture(api_developer, context)
    use_fixture(auth_test_application, context)
    use_fixture(registered_user_on_test_application, context)


def before_scenario(context, scenario):
    pass
