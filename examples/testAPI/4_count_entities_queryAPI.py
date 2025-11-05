import logging
# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_pe import *
# Importing the API exception
from tb_rest_client.rest import ApiException
# Import EntityType for defining entity filters
from tb_rest_client.models.models_pe import EntityFilter, EntityCountQuery


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# ThingsBoard REST API URL
url = "https://development.akiot.es/"

# Default Tenant Administrator credentials
username = "tenant@akiot.es"
password = "tenant"


# Creating the REST client object with context manager to get auto token refresh
with RestClientPE(base_url=url) as rest_client:
    try:
        rest_client.login(username=username, password=password)
        # Create entity filter to get all devices
        # known type ids = [apiUsageState, assetSearchQuery, assetType, deviceSearchQuery, deviceType, edgeSearchQuery, edgeType, entitiesByGroupName, entityGroup, entityGroupList, entityGroupName, entityList, entityName, entityType, entityViewSearchQuery, entityViewType, relationsQuery, schedulerEvent, singleEntity, stateEntity, stateEntityOwner]
        entity_filter = EntityFilter(type="deviceType")

        # Create entity count query with provided filter
        devices_query = EntityCountQuery(entity_filter)

        # Execute entity count query and get total devices count
        devices_count = rest_client.count_entities_by_query(devices_query)
        logging.info("Total devices: \n%r", devices_count)
    except ApiException as e:
        logging.exception(e)
