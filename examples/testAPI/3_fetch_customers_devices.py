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
            user = rest_client.get_user()
            # devices = rest_client.get_customer_device_infos(customer_id=CustomerId(user.id.id, 'CUSTOMER'),
            #                                                 page_size=10,
            #                                                 page=0)
            # Customer Cristian Aranda: 39c4f3a0-b336-11f0-9661-1da9e45f2bbc
            devices = rest_client.get_customer_device_infos(customer_id=CustomerId('39c4f3a0-b336-11f0-9661-1da9e45f2bbc', 'CUSTOMER'),
                                                            page_size=10,
                                                            page=0)

            # Puedo traer los customers asociados a tenants
            users= rest_client.get_user_customers(  page_size=10,
                                                    page=0)
            logging.info("Devices: \n%r", devices)
            logging.info("Customers: \n%r", users)
        except ApiException as e:
            logging.exception(e)


if __name__ == '__main__':
    main()