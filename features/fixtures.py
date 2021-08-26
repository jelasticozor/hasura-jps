import os
import random

from behave import fixture
from jelastic_client import JelasticClientFactory


@fixture
def random_seed(context):
    random.seed('jelasticozor-infrastructure-tests')


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
def clear_environment(context):
    yield
    if hasattr(context, 'current_env_name'):
        env_info = context.control_client.get_env_info(
            context.current_env_name)
        if env_info.exists():
            context.control_client.delete_env(context.current_env_name)


@fixture
def serverless_manifest(context):
    context.serverless_manifest = os.path.join(
        context.project_root_folder, 'serverless', 'manifest.jps')
    return context.serverless_manifest


fixtures_registry = {

}
