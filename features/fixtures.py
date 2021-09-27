import os
import random

from behave import fixture
from jelastic_client import JelasticClientFactory
from test_utils import get_new_random_env_name

from features.utils.faas_client import FaasClientFactory
from features.utils.hasura_client import HasuraClientFactory


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
def api_clients(context):
    userdata = context.config.userdata
    api_url = userdata['api-url']
    api_token = userdata['api-token']
    api_client_factory = JelasticClientFactory(api_url, api_token)
    context.jps_client = api_client_factory.create_jps_client()
    context.control_client = api_client_factory.create_control_client()
    context.file_client = api_client_factory.create_file_client()


@fixture
def faas_port(context):
    context.faas_port = 8080
    return faas_port


@fixture
def path_to_serverless_functions(context):
    context.path_to_serverless_functions = os.path.join(
        context.project_root_folder, 'features', 'data', 'functions')
    return context.path_to_serverless_functions


@fixture
def faas_definition_yaml(context):
    context.faas_definition_yaml = 'faas.yml'
    return context.faas_definition_yaml


@fixture
def faas_client_factory(context):
    context.faas_client_factory = FaasClientFactory(
        context.path_to_serverless_functions,
        context.faas_port,
        context.faas_definition_yaml)
    return context.faas_client_factory


@fixture
def new_environment(context):
    context.current_env_name = get_new_random_env_name(
        context.control_client, context.commit_sha, context.worker_id)
    yield context.current_env_name
    env_info = context.control_client.get_env_info(
        context.current_env_name)
    if env_info.exists():
        context.control_client.delete_env(context.current_env_name)


@fixture
def main_manifest(context):
    context.main_manifest = os.path.join(
        context.project_root_folder, 'manifest.yml')
    return context.main_manifest


@fixture
def serverless_manifest(context):
    context.serverless_manifest = os.path.join(
        context.project_root_folder, 'serverless', 'manifest.yml')
    return context.serverless_manifest


@fixture
def test_manifests_folder(context):
    context.test_manifests_folder = os.path.join(
        context.project_root_folder, 'features', 'data', 'manifests')
    return context.test_manifests_folder


@fixture
def hasura_database_name(context):
    context.hasura_database_name = 'hasura'
    return context.hasura_database_name


@fixture
def fusionauth_database_name(context):
    context.fusionauth_database_name = 'fusionauth'
    return context.fusionauth_database_name


@fixture
def database_user(context):
    context.database_user = 'hasura_user'
    return context.database_user


@fixture
def database_password(context):
    context.database_password = 'admin_password'
    return context.database_password


@fixture
def close_database_connections(context):
    yield
    if hasattr(context, 'connections'):
        for database_connection in context.connections.values():
            database_connection.close()


@fixture
def hasura_projects_folder(context):
    context.hasura_projects_folder = os.path.join(
        context.project_root_folder, 'features', 'data', 'database')
    return context.hasura_projects_folder


@fixture
def hasura_client_factory(context):
    context.hasura_client_factory = HasuraClientFactory(
        'default')
    return context.hasura_client_factory


@fixture
def hasura_internal_port(context):
    context.hasura_internal_port = '8080'
    return context.hasura_internal_port


fixtures_registry = {

}
