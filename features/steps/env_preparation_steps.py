from jelastic_client import NodeSettings, EnvSettings, DockerSettings
from test_utils import get_new_random_env_name


@given(
    u'a jelastic environment with a docker node is available in group \'{node_group}\' with image \'{docker_image}\'')
def step_impl(context, node_group, docker_image):
    node_type = 'docker'
    context.current_env_name = get_new_random_env_name(
        context.control_client, context.commit_sha, context.worker_id)
    env = EnvSettings(shortdomain=context.current_env_name)
    docker_settings = DockerSettings(image=docker_image, nodeGroup=node_group)
    node = NodeSettings(docker=docker_settings,
                        flexibleCloudlets=16, nodeType=node_type)
    created_env_info = context.control_client.create_environment(env, [node])
    assert created_env_info.is_running()
