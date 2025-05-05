import json
import requests

from .models import Joueur,Entraineur,Equipe

def process_webhook_payload(payload):
    type_objet = payload.get("type")
    action = payload.get("action")
    id_objet = payload.get("id")

    print("🔔 Webhook reçu :")
    print(json.dumps(payload, indent=4))

    
    try:
        if action == "delete":
            delete_in_base(id_objet,type_objet)
        elif action == "update":
            endpoint = get_endpoint(id_objet,type_objet,payload)
            print(endpoint)
            response = requests.get(endpoint, json=payload)
            print("🔔 Réponse API reçu :")
            data = response.json()
            print(json.dumps(data, indent=7))
            ajout_element_en_base(data,type_objet)
            if response.status_code==200:
                print(f" Appel API vers {endpoint} — Code {response.status_code} ✅")
            else:
                print(f" Appel API vers {endpoint} — Code {response.status_code} ❌")
        else:
            print("❓ Action non reconnue")
            return
    except requests.RequestException as e:
        print(f"❌ Erreur API : {e}")


def ajout_element_en_base(data,type_data):
    
    if type_data=="joueur":
        Joueur.objects.update_or_create(
                        id_J=data.get("id"),
                        defaults={
                            "nom": data["nom"],
                            "age": data["age"],
                            "poste": data["poste"],
                            "nationalite": data["nationalite"],
                            "pied_fort": data["pied_fort"],
                            "nombre_but": data["nombre_but"],
                        }
                    )
        print("✅ Joueur mis à jour dans la base locale")

    elif type_data=="entraineur":
        Entraineur.objects.update_or_create(
                        id_En=data.get("id"),
                        defaults={
                            "nom": data["nom"],
                            "experience" :data["experience"],
                            "nationalite": data["nationalite"],
                        }
                    )
        print("✅ Entraineur mis à jour dans la base locale")

    elif type_data == "equipe":
        entraineur_data = data.get("entraineur")
        entraineur_id = entraineur_data.get("id_En") if entraineur_data else None

        try:
            entraineur_instance = Entraineur.objects.get(id_En=entraineur_id) if entraineur_id else None
        except Entraineur.DoesNotExist:
            print(f"❌ Entraîneur avec l'id {entraineur_id} non trouvé.")
            entraineur_instance = None

        joueurs_ids = [joueur["id_J"] for joueur in data.get("joueurs", [])]
        joueurs_instances = Joueur.objects.filter(id_J__in=joueurs_ids)

        equipe, created = Equipe.objects.update_or_create(
            id=data.get("id"),
            defaults={
                "nom": data["nom"],
                "stade": data["stade"],
                "entraineur": entraineur_instance
            }
        )

        # Mise à jour ManyToMany des joueurs
        equipe.joueurs.set(joueurs_instances)
        print("✅ Équipe mise à jour dans la base locale")



def delete_in_base(id_object,type_data):
        
        if type_data=="joueur":
            Joueur.objects.filter(id_J=id_object).delete()
            print("✅ Joueur supprimé dans la base locale")
        elif type_data=="entraineur":
            Entraineur.objects.filter(id_En=id_object).delete()
            print("✅ Entraineur supprimé dans la base locale")
        elif type_data=="equipe":
            Equipe.objects.filter(id=id_object).delete()
            print("✅ Equipe supprimé dans la base locale")


def get_endpoint(id_objet,type_objet,payload):
    base_url = "http://127.0.0.1:8000"

    nom = payload.get("nom")

    endpoint_map = {
        "joueur": f"{base_url}/joueurs/{id_objet}/",
        "entraineur": f"{base_url}/entraineurs/{id_objet}/",
        "equipe": f"{base_url}/equipes/{id_objet}/"
    }

    endpoint = endpoint_map.get(type_objet)
    if not endpoint:
        print("❓ Type non reconnu")
        return
 
    return endpoint
    