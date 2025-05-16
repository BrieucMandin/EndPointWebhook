# EndPointWebhook

Se projet fonctionne en paire avec un autre projet dinsponible sur mon github (Essaie_WebHook).


## Environnement de développement 

Pour lancer un environnement, il faut se placer à la racine du projet, où se trouve le fichier `docker-compose.yml`, puis exécuter la commande :

```
docker-compose up -d
```

### Accès à la machine

Pour accéder au container, il suffit de lancer la commande :

```
docker exec -ti endpoint-app bash
```

### Lancement des commandes principales

Pour faire le migrate :
```
python manage.py migrate
```

Créer un super utilisateur :
```
python manage.py createsuperuser
```

Pour lancer un runserver, il faut exécuter la commande suivante :
```
python manage.py runserver 0.0.0.0:8080
```

Il est possible de se connecter au dashboard d'administration django ici : http://127.0.0.1:8000/admin
