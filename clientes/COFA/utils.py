from tb_rest_client.rest_client_pe import *
from tb_rest_client.rest import ApiException
import logging
def creating_asset( rest_client,
                    name,
                    id_farmacia,
                    profile_asset_to_use,
                    customer,direccion,latitud,longitud,cuit_farmacia, responsable, correo, celular):


# Creating an Asset
    
    asset = Asset(name=name, label=id_farmacia,
                asset_profile_id=profile_asset_to_use,
                customer_id=customer.id)
    asset = rest_client.save_asset(asset)

    # Cargo los atributos de servidor del ASSET Farmacia
    body_to_attributes = {
        "correo": correo,
        "direccion": direccion,
        # "imagenEdificio": imagenEdificio,
        "latitud": latitud,
        "longitud": longitud,
        "personaContacto": responsable,
        "telefono": celular,
        "identificador_farmacia": id_farmacia,
        "cuit_farmacia": cuit_farmacia

    }


    # Guardo los atributos de servidor para este asset
    try:
        result = rest_client.telemetry_controller.save_entity_attributes_v1_using_post(
            entity_type="ASSET",
            entity_id=asset.id,
            scope="SERVER_SCOPE",
            body=body_to_attributes
        )
        print("✅ Atributo guardado correctamente:", result)
    except ApiException as e:
        print("❌ Error al guardar atributo:", e)
    
    logging.info("Asset was created:\n%r\n", asset)
    


