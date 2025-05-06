from django.conf import settings


def get_endpoint(type_objet, id_objet):
    base_url = settings.REMOTE_API_BASE_URL

    base_url = "http://127.0.0.1:8000"

    endpoint_map = {
        "joueur": f"{base_url}/joueurs/{id_objet}/",
        "entraineur": f"{base_url}/entraineurs/{id_objet}/",
        "equipe": f"{base_url}/equipes/{id_objet}/"
    }

    return endpoint_map.get(type_objet)
    