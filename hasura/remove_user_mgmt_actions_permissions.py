import argparse

import yaml

non_anonymous_actions = ['validate_token', 'refresh_jwt']


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def main(roles_to_keep, path_to_actions_file):
    with open(path_to_actions_file, 'r') as input_file:
        original_yaml_content = input_file.read()

        roles = set(roles_to_keep.split(';'))

        yaml_data = yaml.load(original_yaml_content, yaml.Loader)
        actions = yaml_data['actions']
        for action in actions:
            if action['name'] not in non_anonymous_actions:
                continue
            if 'permissions' in action:
                current_roles = set(permission['role']
                                    for permission in action['permissions'])
                updated_roles = roles.intersection(current_roles)
                action['permissions'] = [{
                    'role': role
                } for role in updated_roles]
        new_yaml_content = yaml.dump(yaml_data, Dumper=NoAliasDumper)

    with open(path_to_actions_file, 'w') as output_file:
        output_file.write(new_yaml_content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--roles-to-keep', required=True,
                        type=str, action='store')
    parser.add_argument('--actions-file', required=True,
                        type=str, action='store')
    args = parser.parse_args()

    main(args.roles_to_keep, args.actions_file)
