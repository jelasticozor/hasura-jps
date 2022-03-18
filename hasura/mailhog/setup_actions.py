import argparse

import yaml


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def main(actions_yaml):
    with open(actions_yaml, 'r') as input_file:
        original_yaml_content = input_file.read()

        yaml_data = yaml.load(original_yaml_content, yaml.Loader)

        actions = yaml_data['actions']

        for action_name in ['get_emails', 'delete_all_emails', 'delete_email']:
            actions.append({
                'name': action_name,
                'definition': {
                    'kind': 'synchronous',
                    'handler': f"http://{{FAAS_HOSTNAME}}:{{FAAS_PORT}}/function/{action_name.replace('_', '-')}"
                }
            })

        custom_types = yaml_data['custom_types']
        for output_type in ['get_emails_response', 'delete_all_emails_response', 'delete_email_response']:
            custom_types['objects'].append({
                'name': output_type
            })

        new_yaml_content = yaml.dump(yaml_data, Dumper=NoAliasDumper)

    with open(actions_yaml, 'w') as output_file:
        output_file.write(new_yaml_content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--actions-yaml', required=True,
                        type=str, action='store')
    args = parser.parse_args()

    main(args.actions_yaml)
