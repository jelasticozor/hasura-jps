from jelastic_client import NodeSettings, EnvSettings
from test_utils import get_new_random_env_name


@given(u'a jelastic environment with a node of type \'{node_type}\' is available')
def step_impl(context, node_type):
    context.current_env_name = get_new_random_env_name(
        context.control_client, context.commit_sha, context.worker_id)
    env = EnvSettings(shortdomain=context.current_env_name)
    node = NodeSettings(flexibleCloudlets=4, nodeType=node_type)
    created_env_info = context.control_client.create_environment(env, [node])
    assert created_env_info.is_running()
