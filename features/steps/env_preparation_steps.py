import os

from features.utils.manifest_data import get_manifest_data
from features.utils.test_manifest import TestManifest


@given(
    u'a jelastic environment with {node_count:d} {node_type} node is available in node group \'{node_group}\' with image \'{docker_image}\'')
@given(
    u'a jelastic environment with {node_count:d} {node_type} nodes is available in node group \'{node_group}\' with image \'{docker_image}\'')
def step_impl(context, node_count, node_type, node_group, docker_image):
    manifest_filename = os.path.join(
        context.test_manifests_folder, f'{node_type}-node.yml')
    test_manifest = TestManifest(manifest_filename)
    success_text = context.jps_client.install(
        test_manifest.get_content(
            node_count=node_count, node_group=node_group, docker_image=docker_image),
        context.current_env_name)
    context.manifest_data = get_manifest_data(success_text)


@given(u'a jelastic environment with {node_count:d} {node_type} node is available in node group \'{node_group}\'')
@given(u'a jelastic environment with {node_count:d} {node_type} nodes is available in node group \'{node_group}\'')
def step_impl(context, node_count, node_type, node_group):
    manifest_filename = os.path.join(
        context.test_manifests_folder, f'{node_group}-node.yml')
    test_manifest = TestManifest(manifest_filename)
    success_text = context.jps_client.install(
        test_manifest.get_content(node_count=node_count, node_type=node_type),
        context.current_env_name)
    context.manifest_data = get_manifest_data(success_text)
