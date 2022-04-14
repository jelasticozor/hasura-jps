import argparse

from fusionauth.fusionauth_client import FusionAuthClient


def get_default_tenant_id(client):
    response = client.retrieve_tenants()
    assert response.was_successful()

    tenants = response.success_response['tenants']
    default_tenant = [
        tenant for tenant in tenants if tenant['name'] == 'Default'][0]

    return default_tenant['id']


def main(tenant_id, hostname, port, username, password, enable_ssl):
    request = {
        'tenant': {
            'emailConfiguration': {
                'host': hostname,
                'port': port,
                'username': username,
                'password': password,
                'security': 'SSL' if enable_ssl == 'True' else 'NONE',
            }
        }
    }
    client.update_tenant(tenant_id, request)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-url', required=True, type=str, action='store')
    parser.add_argument('--api-key', required=True, type=str, action='store')
    parser.add_argument('--mail-server-host', required=True,
                        type=str, action='store')
    parser.add_argument('--mail-server-port', required=True,
                        type=int, action='store')
    parser.add_argument('--mail-server-username',
                        default='', type=str, action='store')
    parser.add_argument('--mail-server-password',
                        default='', type=str, action='store')
    parser.add_argument('--mail-server-enable-ssl',
                        choices=('True', 'False'), action='store')

    args = parser.parse_args()

    client = FusionAuthClient(args.api_key, args.api_url)
    tenant_id = get_default_tenant_id(client)

    main(tenant_id,
         args.mail_server_host,
         args.mail_server_port,
         args.mail_server_username,
         args.mail_server_password,
         args.mail_server_enable_ssl)
