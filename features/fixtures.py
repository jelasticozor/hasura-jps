import random

from behave import fixture
from jelastic_client import JelasticClientFactory


@fixture
def random_seed(context):
    random.seed('jelasticozor-infrastructure-tests')


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
def clear_environment(context):
    yield
    if hasattr(context, 'current_env_name'):
        print(f'clearing environment <{context.current_env_name}>')
        env_info = context.control_client.get_env_info(
            context.current_env_name)
        if env_info.exists():
            context.control_client.delete_env(context.current_env_name)


fixtures_registry = {

}
