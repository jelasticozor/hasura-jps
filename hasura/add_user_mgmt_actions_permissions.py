import argparse

import yaml


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def main(roles, path_to_actions_file):
    with open(path_to_actions_file, 'r') as input_file:
        original_yaml_content = input_file.read()

        permissions = [{
            'role': role
        } for role in roles.split(';')]

        yaml_data = yaml.load(original_yaml_content, yaml.Loader)
        actions = [action for action in yaml_data['actions']
                   if action['name'] != 'sign_in']
        for action in actions:
            if 'permissions' not in action:
                action['permissions'] = permissions
            else:
                for permission in permissions:
                    if permission not in action['permissions']:
                        action['permissions'].append(permission)
        new_yaml_content = yaml.dump(yaml_data, Dumper=NoAliasDumper)

    with open(path_to_actions_file, 'w') as output_file:
        output_file.write(new_yaml_content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--roles', required=True, type=str, action='store')
    parser.add_argument('--actions-file', required=True,
                        type=str, action='store')
    args = parser.parse_args()

    main(args.roles, args.actions_file)
