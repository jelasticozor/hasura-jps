from jelastic_client import NodeSettings, EnvSettings, DockerSettings


@given(
    u'a jelastic environment with {node_count:d} docker nodes is available in group \'{node_group}\' with image \'{docker_image}\'')
@given(
    u'a jelastic environment with {node_count:d} docker node is available in group \'{node_group}\' with image \'{docker_image}\'')
def step_impl(context, node_count, node_group, docker_image):
    node_type = 'docker'
    env = EnvSettings(shortdomain=context.current_env_name)
    docker_settings = DockerSettings(image=docker_image, nodeGroup=node_group)
    node = NodeSettings(count=node_count, docker=docker_settings,
                        flexibleCloudlets=16, nodeType=node_type)
    created_env_info = context.control_client.create_environment(env, [node])
    assert created_env_info.is_running()


@given(u'a jelastic environment with {node_count:d} {node_type} node in node group \'{node_group}\' is available')
@given(u'a jelastic environment with {node_count:d} {node_type} nodes in node group \'{node_group}\' is available')
def step_impl(context, node_count, node_group, docker_image):
    raise NotImplemented('step not implemented')
