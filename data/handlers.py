import json
import requests

from data.services import delete_in_base, update_or_create_object
from data.api_client import fetch_data
from data.endpoints import get_endpoint


def process_webhook_payload(payload):
    """
    Traite la charge utile (payload) d'un webhook en fonction du type d'action spécifiée.

    Cette fonction prend un dictionnaire contenant les informations d'un webhook, 
    puis effectue l'action appropriée :
    - Si `action` est `"delete"`, l'objet correspondant est supprimé de la base locale.
    - Si `action` est `"update"`, les données à jour sont récupérées via une API 
      et l'objet est mis à jour ou créé dans la base locale.
    - Si `action` est inconnue, un message d'information est affiché.

    Les informations sont affichées dans la console à des fins de suivi.

    :param dict payload: Dictionnaire contenant les données du webhook. Doit contenir les clés 
                         `"type"` (str), `"action"` (str) et `"id"` (int ou str).

    :raises requests.RequestException: En cas d'erreur lors de l'appel à l'API.
    :raises Exception: En cas d'erreur inattendue lors du traitement du webhook.

    :Example:

    >>> payload = {
    ...     "type": "joueur",
    ...     "action": "update",
    ...     "id": 123
    ... }
    >>> process_webhook_payload(payload)
    """
    type_objet = payload.get("type")
    action = payload.get("action")
    id_objet = payload.get("id")

    print("🔔 Webhook reçu :")
    print(json.dumps(payload, indent=4))

    try:
        if action == "delete":
            print(f"🗑️ Suppression demandée pour {type_objet} avec ID {id_objet}")
            delete_in_base(id_objet, type_objet)
            print("✅ Suppression effectuée dans la base locale")

        elif action == "update":
            print(f"🔄 Mise à jour demandée pour {type_objet} avec ID {id_objet}")
            endpoint = get_endpoint(type_objet, id_objet)
            print(f"📡 Endpoint construit : {endpoint}")

            data = fetch_data(endpoint)
            print("🔔 Données récupérées depuis l'API :")
            print(json.dumps(data, indent=4))

            update_or_create_object(data, type_objet)

        else:
            print("❓ Action non reconnue :", action)

    except requests.RequestException as e:
        print(f"❌ Erreur API : {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue lors du traitement du webhook : {e}")
