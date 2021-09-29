import re

base_url_regex = re.compile(r'baseUrl: (.*)\n')


def get_base_url_from_manifest_content(manifest_content):
    match_object = base_url_regex.search(manifest_content)
    return match_object.group(1)
