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
def jelastic_region(context):
    userdata = context.config.userdata
    context.jelastic_region = userdata['jelastic-region']
    return context.jelastic_region


@fixture
def cluster_type(context):
    userdata = context.config.userdata
    context.cluster_type = userdata['cluster-type']
    return context.cluster_type


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


def get_mail_server_definition(env_info, smtp_settings):
    mail_server_nodes = env_info.get_nodes(node_group='mail')
    assert len(mail_server_nodes) == 1, \
        f'expected environment {env_info.env_name()} to have a node group \'mail\''
    mail_server_node = mail_server_nodes[0]
    mail_server_definition = {
        'ip': mail_server_node.int_ip,
        'port': 1025,
    }
    mail_server_definition.update(smtp_settings)
    return mail_server_definition


def create_jelastic_environment(context, settings):
    control_client = context.jelastic_clients_factory.create_control_client()
    context.current_env_name = context.cluster_type + "-" + get_new_random_env_name(
        control_client, context.commit_sha, context.worker_id)
    main_manifest = os.path.join(
        context.project_root_folder, 'manifest.yml')
    jps_client = context.jelastic_clients_factory.create_jps_client()
    print(
        f'installing environment {context.current_env_name} on region {context.jelastic_region} with settings: {settings}')
    success_text = jps_client.install_from_file(
        main_manifest, context.current_env_name, settings=settings, region=context.jelastic_region)
    context.current_env_info = control_client.get_env_info(
        context.current_env_name)
    assert context.current_env_info.is_running(), \
        f'environment {context.current_env_name} is not running'
    context.manifest_data = get_manifest_data(success_text)
    if context.cluster_type == 'dev':
        smtp_settings = {
            'username': '',
            'password': ''
        }
        context.current_mail_server = get_mail_server_definition(
            context.current_env_info, smtp_settings)
    return context.current_env_name


def delete_current_jelastic_environment(context):
    control_client = context.jelastic_clients_factory.create_control_client()
    env_info = control_client.get_env_info(
        context.current_env_name)
    if env_info.exists():
        control_client.delete_env(context.current_env_name)


def get_mail_server_settings(context):
    settings = {
        'mailServerHost': context.current_mail_server['ip'],
        'mailServerPort': context.current_mail_server['port'],
        'mailServerUsername': context.current_mail_server['username'],
        'mailServerPassword': context.current_mail_server['password'],
        'mailServerEnableSsl': False
    }
    return settings


@fixture
def jelastic_environment(context):
    settings = {
        'graphqlEngineImage': f'{context.graphql_engine_image}:{context.commit_sha}',
        'useAutoGeneratedHasuraAdminSecret': False,
        'hasuraAdminSecret': context.hasura_admin_secret,
        'fusionauthVersion': context.fusionauth_version,
        'useJelasticEmailAsAuthAdminEmail': False,
        'authAdminEmail': context.fusionauth_admin_email,
        'authIssuer': context.fusionauth_issuer,
        'fncTag': context.commit_sha,
        'clusterType': context.cluster_type,
    }
    if context.cluster_type == 'prod':
        settings_prod = get_mail_server_settings(context)
        settings.update(settings_prod)
    yield create_jelastic_environment(
        context, settings)
    delete_current_jelastic_environment(context)


@fixture
def jelastic_environment_with_automatic_settings(context):
    settings = {
        'graphqlEngineImage': f'{context.graphql_engine_image}:{context.commit_sha}',
        'useAutoGeneratedHasuraAdminSecret': True,
        'hasuraAdminSecret': context.hasura_admin_secret,
        'fusionauthVersion': context.fusionauth_version,
        'useJelasticEmailAsAuthAdminEmail': True,
        'authIssuer': context.fusionauth_issuer,
        'fncTag': context.commit_sha,
        'clusterType': context.cluster_type,
    }
    if context.cluster_type == 'prod':
        settings_prod = get_mail_server_settings(context)
        settings.update(settings_prod)
    yield create_jelastic_environment(
        context, settings)
    delete_current_jelastic_environment(context)


@fixture
def add_application_manifest_file(context):
    context.add_application_manifest_file = os.path.join(
        context.project_root_folder, 'add-application.yml')


@fixture
def remove_application_manifest_file(context):
    context.remove_application_manifest_file = os.path.join(
        context.project_root_folder, 'remove-application.yml')


@fixture
def api_developer(context):
    # TODO: use context.current_mail_server
    context.api_developer = ApiDeveloper(
        context.jelastic_clients_factory,
        context.current_env_info,
        context.manifest_data,
        context.add_application_manifest_file,
        context.remove_application_manifest_file)
    yield context.api_developer
    del context.api_developer


@fixture
def remove_applications(context):
    context.app_ids = []
    yield
    if len(context.app_ids) > 0:
        for app_id in context.app_ids:
            context.api_developer.delete_application(app_id)
        assert context.api_developer.no_application_exists()


@fixture
def auth_test_application(context):
    context.auth_test_application = context.api_developer.create_application(
        'test-application', ['user'])
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
        'user'
    ])
    yield context.registered_user_on_test_application
    context.api_developer.delete_registration(
        user_id, test_application_id)
    context.api_developer.delete_user(user_id)


@fixture
def external_mail_server(context):
    control_client = context.jelastic_clients_factory.create_control_client()
    env_name = "mail-server" + "-" + get_new_random_env_name(
        control_client, context.commit_sha, context.worker_id)
    manifest = os.path.join(
        context.project_root_folder, 'features', 'data', 'jelastic', 'external-mail-server.yml')
    jps_client = context.jelastic_clients_factory.create_jps_client()
    settings = {
        'username': 'smtp-user',
        'password': 'smtp-password'
    }
    print(
        f'installing environment {env_name} on region {context.jelastic_region} with settings: {settings}')
    jps_client.install_from_file(
        manifest, env_name, settings=settings, region=context.jelastic_region)
    env_info = control_client.get_env_info(env_name)
    assert env_info.is_running()
    context.current_mail_server = get_mail_server_definition(
        env_info, settings)
    yield context.current_mail_server
    env_info = control_client.get_env_info(env_name)
    if env_info.exists():
        control_client.delete_env(env_name)


fixtures_registry = {
    'jelastic-env': jelastic_environment,
    'jelastic-env-with-automatic-settings': jelastic_environment_with_automatic_settings,
    'api-developer': api_developer,
    'auth-test-application': auth_test_application,
    'registered-user-on-test-application': registered_user_on_test_application,
}
