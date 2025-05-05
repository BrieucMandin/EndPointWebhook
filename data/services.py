import json
import requests

def process_webhook_payload(payload):
    type_objet = payload.get("type")
    action = payload.get("action")
    id_objet = payload.get("id")

    print("🔔 Webhook reçu :")
    print(json.dumps(payload, indent=4))

    base_url = "http://127.0.0.1:8000/"

    endpoint_map = {
        "joueur": f"{base_url}/joueurs/{id_objet}/",
        "entraineur": f"{base_url}/entraineurs/{id_objet}/",
        "equipe": f"{base_url}/equipes/{id_objet}/"
    }

    endpoint = endpoint_map.get(type_objet)
    if not endpoint:
        print("❓ Type non reconnu")
        return

    try:
        if action == "delete":
            #response = requests.delete(endpoint)
            pass
        elif action == "update":
            response = requests.get(endpoint, json=payload)
        else:
            print("❓ Action non reconnue")
            return
        if response.status_code==200:
            print(f" Appel API vers {endpoint} — Code {response.status_code} ✅")
            print("🔔 Réponse API reçu :")
            print(json.dumps(response.json(), indent=7))
        else:
            print(f" Appel API vers {endpoint} — Code {response.status_code} ❌")
    except requests.RequestException as e:
        print(f"❌ Erreur API : {e}")
