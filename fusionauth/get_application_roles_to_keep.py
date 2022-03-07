import argparse

from fusionauth.fusionauth_client import FusionAuthClient


def main(client, app_id):
    response = client.retrieve_applications()
    assert response.was_successful(), \
        f'unable to retrieve all applications'
    applications = response.success_response['applications']
    roles = [role['name'] for application in applications if application['id'] != app_id for role in
             application['roles']]
    return set(roles)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-url', required=True, type=str, action='store')
    parser.add_argument('--api-key', required=True, type=str, action='store')
    parser.add_argument('--app-id', required=True, type=str, action='store')
    args = parser.parse_args()

    client = FusionAuthClient(args.api_key, args.api_url)

    roles_to_keep = main(client, args.app_id)
    print(';'.join(roles_to_keep))
