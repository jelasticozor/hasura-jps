import os


@given(
    u'a jelastic environment with {node_count:d} {node_type} node is available in node group \'{node_group}\' with image \'{docker_image}\'')
@given(
    u'a jelastic environment with {node_count:d} {node_type} nodes is available in node group \'{node_group}\' with image \'{docker_image}\'')
def step_impl(context, node_count, node_type, node_group, docker_image):
    manifest_filename = os.path.join(
        context.test_manifests_folder, f'{node_type}-node.yml')

    with open(manifest_filename) as manifest_file:
        manifest_content = manifest_file.read()

        # TODO: create a test manifest class where we abstract out this logic:
        manifest_content.replace("NODE_COUNT", node_count)
        manifest_content.replace("NODE_GROUP", node_group)
        manifest_content.replace("DOCKER_IMAGE", docker_image)

        context.jps_client.install(manifest_content)


@given(u'a jelastic environment with {node_count:d} {node_type} node is available in node group \'{node_group}\'')
@given(u'a jelastic environment with {node_count:d} {node_type} nodes is available in node group \'{node_group}\'')
def step_impl(context, node_count, node_type, node_group):
    manifest_filename = os.path.join(
        context.test_manifests_folder, f'{node_group}-node.yml')

    with open(manifest_filename) as manifest_file:
        manifest_content = manifest_file.read()

        # TODO: create a test manifest class where we abstract out this logic:
        manifest_content.replace("NODE_COUNT", node_count)
        manifest_content.replace("NODE_TYPE", node_type)

        context.jps_client.install(manifest_content)
