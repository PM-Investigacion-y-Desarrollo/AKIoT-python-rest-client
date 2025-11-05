# Creo un perfil para los activos
from tb_rest_client.models.models_pe import AssetProfile, EntityId
import logging
from pprint import pprint

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
try:
    # 1.1 Intentar obtener perfiles de activos para verificar si ya existe
    # El método get_asset_profiles es paginado, por lo que buscamos en la primera página
    page_data = rest_client.get_asset_profiles(page_size=100, page=0, text_search=profile_name)

    existing_profile = next((profile for profile in page_data.data if profile.name == profile_name), None)

    if existing_profile:
        logging.info(f"El perfil de activo '{profile_name}' ya existe. Usando el existente.")
        return existing_profile

    # 1.2 Crear una instancia del modelo AssetProfile
    new_asset_profile = AssetProfile(name=profile_name)

    if profile_description:
        new_asset_profile.description = profile_description

    # NOTA: Otros campos importantes como 'image', 'default_rule_chain_id', 
    # 'provision_device_key', 'profile_data', etc., se pueden configurar aquí.
    # Por simplicidad, se deja con los valores por defecto.

    # 1.3 Guardar el perfil de activo utilizando el método save_asset_profile
    created_profile = rest_client.save_asset_profile(body=new_asset_profile)
    logging.info(f"✅ Perfil de activo '{profile_name}' creado exitosamente.")
    return created_profile
        
    except Exception as e:
        logging.error(f"❌ Error al crear/obtener el perfil de activo: {e}")
        return Non

# ------------------------------------------------------------------------------
from tb_rest_client.models.models_pe import EntityGroup, EntityId, UserId
from tb_rest_client.rest_client_base import RestClientBase
import logging
from pprint import pprint

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- El código de tu clase RestClientPE (RestClientPE) debe estar importado o definido aquí ---
# ... (Se asume que la clase RestClientPE está disponible en el entorno de ejecución) ...
# from rest_client_pe import RestClientPE 

def get_or_create_entity_group(rest_client: RestClientPE, group_name: str, group_type: str) -> EntityGroup:
    """
    Busca un grupo de entidades existente por nombre, tipo y propietario (Tenant). 
    Si no existe, lo crea.
    """
    try:
        # 1. Obtener el ID del propietario (Tenant actual)
        # Asumimos que el cliente ya está logueado, por lo que podemos obtener el tenant_id del usuario actual
        current_user = rest_client.get_current_user()
        owner_id = current_user.tenant_id
        
        if not owner_id:
            raise ValueError("No se pudo obtener el ID del Tenant. Asegúrate de estar logueado como Tenant Admin.")

        # 2. Intentar obtener el grupo de activos por nombre, tipo y propietario
        logging.info(f"Buscando grupo de {group_type} con nombre '{group_name}' para el propietario '{owner_id.id}'...")
        
        existing_group = rest_client.get_entity_group_by_owner_and_name_and_type(
            owner_id=owner_id, 
            group_type=group_type, 
            group_name=group_name
        )
        
        # Si la llamada tiene éxito, el grupo existe
        logging.info(f"✅ ¡Éxito! El grupo de {group_type} '{group_name}' ya existe.")
        return existing_group

    except Exception as e:
        # En la API de ThingsBoard, no encontrar una entidad generalmente resulta en una excepción (p. ej., HTTP 404).
        # Esto es un patrón común para indicar que se debe proceder a crearlo.
        # En una implementación robusta, se verificaría el código de error (p. ej., 404 Not Found).

        # Si el error NO es un 404 de "entidad no encontrada", podríamos querer manejarlo por separado.
        # Simplificamos asumiendo que es un 'no encontrado' si falló la obtención.
        logging.warning(f"El grupo de {group_type} '{group_name}' no existe o hubo un error: {e}. Procediendo a crear...")

        # 3. Si la búsqueda falla (grupo no existe), crear el nuevo grupo
        new_entity_group = EntityGroup(name=group_name, type=group_type)
        
        # El método save_entity_group creará el grupo en el ámbito del usuario logueado
        created_group = rest_client.save_entity_group(body=new_entity_group)
        
        logging.info(f"✅ Grupo de {group_type} creado exitosamente: '{group_name}'")
        return created_group

# ===============================================
# PARTE DE EJECUCIÓN (Ejemplo)
# ===============================================

# ⚠️ Sustituye estos valores con la URL y credenciales reales de tu instancia de ThingsBoard
THINGSBOARD_URL = 'http://localhost:8080'
USERNAME = 'tenant@thingsboard.org'
PASSWORD = 'tenant'

try:
    # 0. Inicialización y Autenticación
    rest_client = RestClientPE(THINGSBOARD_URL)
    rest_client.login(USERNAME, PASSWORD) 
    logging.info("Login exitoso.")
    
    # --- Parámetros de la Entidad ---
    group_name = "farmacias_cofa"
    group_type = "ASSET" # Tipo de entidad (ASSET, DEVICE, CUSTOMER, etc.)
    
    # 1. Ejecutar la función para obtener o crear el grupo
    shared_asset_group = get_or_create_entity_group(rest_client, group_name, group_type)
    
    # 2. Mostrar el resultado
    print(f"\n--- Resultado para el grupo '{group_name}' ---")
    pprint(shared_asset_group.to_dict())
    print(f"\nID del Grupo de Activos: {shared_asset_group.id.id}")
    
except Exception as e:
    logging.error(f"❌ Un error ocurrió durante la ejecución: {e}")

finally:
    # 3. Logout (Recomendado)
    if 'rest_client' in locals():
        try:
            rest_client.logout()
            logging.info("Logout exitoso.")
        except:
            # Ignorar errores de logout si la sesión ya expiró o hubo un error previo
            pass