import os
import random

from behave import fixture
from behave.fixture import use_composite_fixture_with, fixture_call_params
from jelastic_client import JelasticClientFactory
from jelastic_client.core import JelasticClientException
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from test_utils import get_new_random_env_name
from test_utils.manifest_data import get_manifest_data

from features.actors.api_developer import ApiDeveloper
from features.actors.api_user import ApiUser


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
def graylog_host(context):
    userdata = context.config.userdata
    context.graylog_host = userdata['graylog-host']
    return context.graylog_host


@fixture
def graylog_port(context):
    userdata = context.config.userdata
    context.graylog_port = userdata['graylog-port']
    return context.graylog_port


@fixture
def docker_hub_registry_user(context):
    userdata = context.config.userdata
    context.docker_hub_registry_user = userdata['docker-hub-registry-user']
    return context.docker_hub_registry_user


@fixture
def docker_hub_registry_password(context):
    userdata = context.config.userdata
    context.docker_hub_registry_password = userdata['docker-hub-registry-password']
    return context.docker_hub_registry_password


def get_mail_server_definition(env_info):
    mail_server_nodes = env_info.get_nodes(node_group='mail')
    assert len(mail_server_nodes) == 1, \
        f'expected environment {env_info.env_name()} to have a node group \'mail\''
    mail_server_node = mail_server_nodes[0]
    mail_server_definition = {
        'ip': mail_server_node.int_ip,
        'port': 1025,
    }
    return mail_server_definition


@retry(reraise=True,
       retry=retry_if_exception_type(JelasticClientException),
       stop=stop_after_attempt(3),
       wait=wait_fixed(60))
def create_jelastic_environment(context, settings):
    control_client = context.jelastic_clients_factory.create_control_client()
    context.current_env_name = context.cluster_type + "-" + get_new_random_env_name(
        control_client, context.commit_sha, context.worker_id)
    context.env_names.append(context.current_env_name)
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
        context.current_mail_server = get_mail_server_definition(
            context.current_env_info)
    return context.current_env_name


def delete_jelastic_environment(context, env_name):
    control_client = context.jelastic_clients_factory.create_control_client()
    env_info = control_client.get_env_info(env_name)
    if env_info.exists():
        control_client.delete_env(env_name)


def get_mail_server_settings(context):
    settings = {
        'mailServerHost': context.current_mail_server['ip'],
        'mailServerPort': context.current_mail_server['port'],
        'mailServerUsername': '',
        'mailServerPassword': '',
        'mailServerEnableSsl': False
    }
    return settings


@fixture
def jelastic_environment(context):
    settings = {
        'graphqlEngineImage': f'{context.graphql_engine_image}:{context.commit_sha}',
        'useAutoGeneratedHasuraAdminSecret': False,
        'hasuraAdminSecret': context.hasura_admin_secret,
        'useJelasticEmailAsAuthAdminEmail': False,
        'authAdminEmail': context.fusionauth_admin_email,
        'authIssuer': context.fusionauth_issuer,
        'hasuraJpsCommitShortSha': context.commit_sha,
        'clusterType': context.cluster_type,
        # if we don't set this optional parameter to True,
        # we need an external domain name, which we don't provide
        # just for the sake of testing
        'useDefaultExternalDomain': True,
        'useExternalGraylog': True,
        'graylogServerHost': context.graylog_host,
        'graylogServerPort': context.graylog_port,
        'useAnonymousDockerHubAccount': False,
        'dockerHubUser': context.docker_hub_registry_user,
        'dockerHubPassword': context.docker_hub_registry_password
    }
    if context.cluster_type == 'prod':
        settings_prod = get_mail_server_settings(context)
        settings.update(settings_prod)
    yield create_jelastic_environment(
        context, settings)
    delete_jelastic_environment(context, context.current_env_name)


@fixture
def jelastic_environment_with_automatic_settings(context):
    settings = {
        'graphqlEngineImage': f'{context.graphql_engine_image}:{context.commit_sha}',
        'useAutoGeneratedHasuraAdminSecret': True,
        'hasuraAdminSecret': context.hasura_admin_secret,
        'useJelasticEmailAsAuthAdminEmail': True,
        'authIssuer': context.fusionauth_issuer,
        'hasuraJpsCommitShortSha': context.commit_sha,
        'clusterType': context.cluster_type,
        # if we don't set this optional parameter to True,
        # we need an external domain name, which we don't provide
        # just for the sake of testing
        'useDefaultExternalDomain': True,
        'useExternalGraylog': True,
        'graylogServerHost': context.graylog_host,
        'graylogServerPort': context.graylog_port,
        'useAnonymousDockerHubAccount': False,
        'dockerHubUser': context.docker_hub_registry_user,
        'dockerHubPassword': context.docker_hub_registry_password
    }
    if context.cluster_type == 'prod':
        settings_prod = get_mail_server_settings(context)
        settings.update(settings_prod)
    yield create_jelastic_environment(
        context, settings)
    delete_jelastic_environment(context, context.current_env_name)


@fixture
def add_application_manifest_file(context):
    context.add_application_manifest_file = os.path.join(
        context.project_root_folder, 'add-application.yml')


@fixture
def remove_application_manifest_file(context):
    context.remove_application_manifest_file = os.path.join(
        context.project_root_folder, 'remove-application.yml')


def path_to_graphql_folder(context):
    return os.path.join(
        context.project_root_folder, 'features', 'data', 'graphql')


@fixture
def api_developer(context):
    context.api_developer = ApiDeveloper(
        context.jelastic_clients_factory,
        context.current_env_info,
        context.manifest_data,
        context.add_application_manifest_file,
        context.remove_application_manifest_file,
        path_to_graphql_folder(context))
    yield context.api_developer
    del context.api_developer


@fixture
def api_user(context):
    endpoint = f'https://{context.current_env_info.domain()}/v1/graphql'
    context.api_user = ApiUser(endpoint, path_to_graphql_folder(context))
    yield context.api_user
    user_id = context.api_user.user_id
    if user_id is not None:
        context.api_developer.delete_user(user_id)
        del context.api_user


@fixture
def remove_applications(context):
    context.app_ids = []
    yield
    if len(context.app_ids) > 0:
        for app_id in context.app_ids:
            context.api_developer.delete_application(app_id)
        assert context.api_developer.no_application_exists()


@fixture
def external_mail_server_environment(context):
    control_client = context.jelastic_clients_factory.create_control_client()
    env_name = "mail-server" + "-" + get_new_random_env_name(
        control_client, context.commit_sha, context.worker_id)
    context.env_names.append(env_name)
    manifest = os.path.join(
        context.project_root_folder, 'features', 'data', 'jelastic', 'external-mail-server.yml')
    jps_client = context.jelastic_clients_factory.create_jps_client()
    print(
        f'installing environment {env_name} on region {context.jelastic_region}')
    jps_client.install_from_file(
        manifest, env_name, region=context.jelastic_region)
    env_info = control_client.get_env_info(env_name)
    assert env_info.is_running()
    context.current_mail_server = get_mail_server_definition(
        env_info)
    yield context.current_mail_server
    env_info = control_client.get_env_info(env_name)
    if env_info.exists():
        control_client.delete_env(env_name)


@fixture
def expose_mailhog_api(context):
    jps_client = context.jelastic_clients_factory.create_jps_client()
    settings = {
        'mailServerHost': context.current_mail_server['ip'],
    }
    manifest = os.path.join(
        context.project_root_folder, 'mailhog', 'expose-api.yml')
    jps_client.install_from_file(
        manifest, context.current_env_name, settings=settings)


@fixture
def test_environment(context):
    fixtures = []
    if context.cluster_type == 'prod':
        fixtures.append(fixture_call_params(external_mail_server_environment))
    fixtures.append(fixture_call_params(jelastic_environment))
    if context.cluster_type == 'prod':
        fixtures.append(fixture_call_params(expose_mailhog_api))
    test_environment = use_composite_fixture_with(context, fixtures)
    return test_environment


@fixture
def test_environment_with_automatic_settings(context):
    fixtures = []
    if context.cluster_type == 'prod':
        fixtures.append(fixture_call_params(external_mail_server_environment))
    fixtures.append(fixture_call_params(
        jelastic_environment_with_automatic_settings))
    if context.cluster_type == 'prod':
        fixtures.append(fixture_call_params(expose_mailhog_api))
    test_environment = use_composite_fixture_with(context, fixtures)
    return test_environment


@fixture
def clean_up_not_deleted_environments(context):
    context.env_names = []
    yield context.env_names
    for env_name in context.env_names:
        delete_jelastic_environment(context, env_name)


fixtures_registry = {
    'test-env': test_environment,
    'test-env-with-automatic-settings': test_environment_with_automatic_settings,
    'api-developer': api_developer,
    'api-user': api_user,
}
