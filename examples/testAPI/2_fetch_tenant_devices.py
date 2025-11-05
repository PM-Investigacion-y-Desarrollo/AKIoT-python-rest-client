import logging
# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_pe import *
# Importing the API exception
from tb_rest_client.rest import ApiException


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# ThingsBoard REST API URL
url = "https://development.akiot.es/"

# Default Tenant Administrator credentials
username = "tenant@akiot.es"
password = "tenant"

def main():
    # Creating the REST client object with context manager to get auto token refresh
    with RestClientPE(base_url=url) as rest_client:
        try:
            rest_client.login(username=username, password=password)
            res = rest_client.get_tenant_devices(page_size=18, page=0)

            logging.info("Device info:\n%r", res)
            pass
        except ApiException as e:
            logging.exception(e)


if __name__ == '__main__':
    main()
