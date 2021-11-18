import argparse
import json
import os
import uuid


def system_configuration(cors_allowed_origins):
    return {
        'body': {
            'systemConfiguration': {
                'corsConfiguration': {
                    'allowedMethods': [
                        'POST'
                    ],
                    'allowedOrigins': cors_allowed_origins
                }
            }
        },
        'method': 'PATCH',
        'url': '/api/system-configuration'
    }


def main(args):
    data = {}
    with open(args.input_kickstart) as file:
        data = json.load(file)
        data['variables']['adminEmail'] = args.admin_email
        data['variables']['adminPassword'] = args.admin_password
        data['variables']['defaultTenantId'] = str(uuid.uuid4())
        data['variables']['hasuraClaimsNamespace'] = args.hasura_claims_namespace
        data['variables']['issuer'] = args.issuer
        data['variables']['almightyApiKey'] = args.almighty_api_key
        data['variables']['serverlessApiKey'] = args.serverless_api_key
        if args.cors_allowed_origins:
            data['requests'].append(system_configuration(
                args.cors_allowed_origins.replace(' ', '').split(',')))
    with open(os.path.join(args.output_kickstart), 'w') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)
        json_file.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--admin-email', required=True,
                        type=str, action='store')
    parser.add_argument('--admin-password', required=True,
                        type=str, action='store')
    parser.add_argument('--almighty-api-key', required=True,
                        type=str, action='store')
    parser.add_argument('--serverless-api-key',
                        required=True, type=str, action='store')
    parser.add_argument('--cors-allowed-origins',
                        default='', type=str, action='store')
    parser.add_argument('--hasura-claims-namespace',
                        default='https://hasura.io/jwt/claims', type=str, action='store')
    parser.add_argument('--issuer', required=True, type=str, action='store')
    parser.add_argument('--input-kickstart', required=True,
                        type=str, action='store')
    parser.add_argument('--output-kickstart', required=True,
                        type=str, action='store')
    args = parser.parse_args()

    main(args)
