import os
import random

from behave import fixture
from jelastic_client import JelasticClientFactory
from test_utils import get_new_random_env_name

from features.utils.faas_client import FaasClientFactory


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
def database_manifest(context):
    context.database_manifest = os.path.join(
        context.project_root_folder, 'database', 'manifest.yml')
    return context.database_manifest


@fixture
def test_manifests_folder(context):
    context.test_manifests_folder = os.path.join(
        context.project_root_folder, 'features', 'data', 'manifests')
    return context.test_manifests_folder


fixtures_registry = {

}
