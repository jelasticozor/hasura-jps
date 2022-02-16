import argparse

from fusionauth.fusionauth_client import FusionAuthClient


def get_hasura_lambda_id(client):
    response = client.retrieve_lambdas_by_type('JWTPopulate')
    assert response.was_successful()

    jwt_lambdas = response.success_response['lambdas']
    lambda_ids = [l['id'] for l in jwt_lambdas if l['name'] == 'hasura']
    assert len(lambda_ids) == 1

    return lambda_ids[0]


def semi_colon_separated_list_to_json_roles(roles):
    role_names = roles.split(';')
    assert len(role_names) > 0
    roles = [{
        'isDefault': False,
        'isSuperRole': False,
        'name': role_name
    } for role_name in role_names]
    roles[0]['isDefault'] = True

    return roles


def create_test_application(client, app_name, roles, lambda_id, app_id=None):
    user_roles = semi_colon_separated_list_to_json_roles(roles)

    response = client.create_application(request={
        'application': {
            'jwtConfiguration': {
                'enabled': True,
                'refreshTokenTimeToLiveInMinutes': 1440,
                'timeToLiveInSeconds': 3600
            },
            'lambdaConfiguration': {
                'accessTokenPopulateId': lambda_id
            },
            'loginConfiguration': {
                'allowTokenRefresh': True,
                'generateRefreshTokens': True,
                'requireAuthentication': True
            },
            'name': app_name,
            'roles': user_roles
        }
    }, application_id=app_id)
    assert response.was_successful() is True, \
        f'unable to create application: {response.exception} ({response.status})'
    return response.success_response['application']['id']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-url', required=True, type=str, action='store')
    parser.add_argument('--api-key', required=True, type=str, action='store')
    parser.add_argument('--app-name', required=True, type=str, action='store')
    parser.add_argument('--app-id', required=False, type=str, action='store')
    parser.add_argument('--roles', required=True, type=str, action='store')
    args = parser.parse_args()

    client = FusionAuthClient(args.api_key, args.api_url)
    lambda_id = get_hasura_lambda_id(client)
    args.app_id = None if args.app_id is None or len(
        args.app_id) == 0 else args.app_id
    app_id = create_test_application(
        client, args.app_name, args.roles, lambda_id, args.app_id)

    print(app_id)
