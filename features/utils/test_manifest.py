class TestManifest:
    def __init__(self, filename):
        with open(filename) as manifest_file:
            self.__content = manifest_file.read()

    def get_content(self, node_count, node_type=None, node_group=None, docker_image=None):
        content = self.__content.replace("NODE_COUNT", str(node_count))
        if node_group is not None:
            content = content.replace("NODE_GROUP", node_group)
        if node_type is not None:
            content = content.replace("NODE_TYPE", node_type)
        if docker_image is not None:
            content = content.replace("DOCKER_IMAGE", docker_image)
        return content
