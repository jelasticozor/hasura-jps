import os
import random

from behave import fixture
from jelastic_client import JelasticClientFactory
from test_utils import get_new_random_env_name
from test_utils.manifest_data import get_manifest_data

from features.actors.api_developer import ApiDeveloper


@fixture
def random_seed(context):
    random.seed('hasura-jps-tests')


@fixture
def worker_id(context):
    context.worker_id = 'master'
    return context.worker_id


@fixture
def commit_sha(context):
    userdata = context.config.userdata
    context.commit_sha = userdata['commit-sha']
    return context.commit_sha


@fixture
def project_root_folder(context):
    userdata = context.config.userdata
    context.project_root_folder = userdata['project-root-folder'] if 'project-root-folder' in userdata else '.'
    return context.project_root_folder


@fixture
def jelastic_clients_factory(context):
    userdata = context.config.userdata
    api_url = userdata['api-url']
    api_token = userdata['api-token']
    context.jelastic_clients_factory = JelasticClientFactory(
        api_url, api_token)
    return context.jelastic_clients_factory


@fixture
def path_to_serverless_test_configuration(context):
    context.path_to_serverless_test_configuration = os.path.join(
        context.project_root_folder, 'features', 'data', 'functions', 'faas.yml')
    return context.path_to_serverless_test_configuration


@fixture
def fusionauth_version(context):
    userdata = context.config.userdata
    context.fusionauth_version = userdata['fusionauth-version']
    return context.fusionauth_version


@fixture
def fusionauth_admin_email(context):
    context.fusionauth_admin_email = 'admin@company.com'
    return context.fusionauth_admin_email


@fixture
def fusionauth_issuer(context):
    context.fusionauth_issuer = 'company.com'
    return context.fusionauth_issuer


@fixture
def hasura_admin_secret(context):
    context.hasura_admin_secret = 'admin'
    return context.hasura_admin_secret


@fixture
def graphql_engine_image(context):
    context.graphql_engine_image = 'softozor/graphql-engine'
    return context.graphql_engine_image


@fixture
def jelastic_environment(context):
    control_client = context.jelastic_clients_factory.create_control_client()
    context.current_env_name = get_new_random_env_name(
        control_client, context.commit_sha, context.worker_id)
    main_manifest = os.path.join(
        context.project_root_folder, 'manifest.yml')
    jps_client = context.jelastic_clients_factory.create_jps_client()
    success_text = jps_client.install_from_file(
        main_manifest, context.current_env_name, settings={
            'graphqlEngineImage': f'{context.graphql_engine_image}:{context.commit_sha}',
            'hasuraAdminSecret': context.hasura_admin_secret,
            'fusionauthVersion': context.fusionauth_version,
            'useJelasticEmailAsAuthAdminEmail': False,
            'authAdminEmail': context.fusionauth_admin_email,
            'authIssuer': context.fusionauth_issuer,
            'fncTag': context.commit_sha
        })
    context.current_env_info = control_client.get_env_info(
        context.current_env_name)
    assert context.current_env_info.is_running()
    context.manifest_data = get_manifest_data(success_text)
    yield context.current_env_name
    env_info = control_client.get_env_info(
        context.current_env_name)
    if env_info.exists():
        control_client.delete_env(context.current_env_name)


@fixture
def api_developer(context):
    context.api_developer = ApiDeveloper(
        context.jelastic_clients_factory, context.current_env_info, context.manifest_data)
    yield context.api_developer
    del context.api_developer


@fixture
def registered_user_role(context):
    context.registered_user_role = 'user'
    return context.registered_user_role


@fixture
def auth_test_application(context):
    context.auth_test_application = context.api_developer.create_test_application(
        context.registered_user_role)
    yield context.auth_test_application
    context.api_developer.delete_application(
        context.auth_test_application)


@fixture
def registered_user_on_test_application(context):
    test_application_id = context.auth_test_application
    context.registered_user_on_test_application = {
        'email': 'user@company.com',
        'password': 'password'
    }
    user_id = context.api_developer.create_user(
        context.registered_user_on_test_application)
    context.api_developer.register_user(user_id, test_application_id, [
        context.registered_user_role
    ])
    yield context.registered_user_on_test_application
    context.api_developer.delete_registration(
        user_id, test_application_id)
    context.api_developer.delete_user(user_id)


fixtures_registry = {}
