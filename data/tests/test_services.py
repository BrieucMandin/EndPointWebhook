# data/tests/test_services.py

from django.test import TestCase

from data.models import Joueur, Entraineur, Equipe
from data.services import update_or_create_object, delete_in_base


class ServicesTests(TestCase):

    def test_update_or_create_joueur_creation(self):
        data = {
            "id_J": 1,
            "nom": "Mbappé",
            "age": 25,
            "poste": "Attaquant",
            "nationalite": "Française",
            "pied_fort": "Droit",
            "nombre_but": 150,
        }

        update_or_create_object(data, "joueur")
        joueur = Joueur.objects.get(id_J=1)
        self.assertEqual(joueur.nom, "Mbappé")

    def test_update_or_create_joueur_update(self):
        joueur = Joueur.objects.create(
            id_J=2, nom="Griezmann", age=32, poste="Milieu", nationalite="Française", pied_fort="Gauche", nombre_but=90
        )

        data = {
            "id_J": 2,
            "nom": "Antoine Griezmann",
            "age": 33,
            "poste": "Milieu",
            "nationalite": "Française",
            "pied_fort": "Gauche",
            "nombre_but": 95,
        }

        update_or_create_object(data, "joueur")
        joueur.refresh_from_db()
        self.assertEqual(joueur.nom, "Antoine Griezmann")
        self.assertEqual(joueur.age, 33)

    def test_delete_joueur(self):
        Joueur.objects.create(
            id_J=3, nom="Test", age=20, poste="Défenseur", nationalite="Brésilienne", pied_fort="Droit", nombre_but=1
        )
        delete_in_base(3, "joueur")
        self.assertEqual(Joueur.objects.filter(id_J=3).count(), 0)

    def test_update_or_create_entraineur(self):
        data = {"id_En": 1, "nom": "Deschamps", "experience": 10, "nationalite": "Française"}

        update_or_create_object(data, "entraineur")
        entraineur = Entraineur.objects.get(id_En=1)
        self.assertEqual(entraineur.nom, "Deschamps")

    def test_delete_entraineur(self):
        Entraineur.objects.create(id_En=2, nom="Test Coach", experience=5, nationalite="Espagnole")
        delete_in_base(2, "entraineur")
        self.assertEqual(Entraineur.objects.filter(id_En=2).count(), 0)

    def test_update_or_create_equipe(self):
        entraineur = Entraineur.objects.create(id_En=5, nom="Zidane", experience=12, nationalite="Française")
        joueur1 = Joueur.objects.create(
            id_J=10,
            nom="Joueur 1",
            age=22,
            poste="Défenseur",
            nationalite="Portugaise",
            pied_fort="Gauche",
            nombre_but=2,
        )
        joueur2 = Joueur.objects.create(
            id_J=11, nom="Joueur 2", age=24, poste="Milieu", nationalite="Italienne", pied_fort="Droit", nombre_but=5
        )

        data = {
            "id_Eq": 1,
            "nom": "PSG",
            "stade": "Parc des Princes",
            "entraineur": {"id_En": 5},
            "joueurs": [{"id_J": 10}, {"id_J": 11}],
        }

        update_or_create_object(data, "equipe")
        equipe = Equipe.objects.get(id_Eq=1)
        self.assertEqual(equipe.nom, "PSG")
        self.assertEqual(equipe.entraineur, entraineur)
        self.assertSetEqual(set(equipe.joueurs.values_list("id_J", flat=True)), {10, 11})

    def test_delete_equipe(self):
        entraineur = Entraineur.objects.create(id_En=100, nom="Test Coach", experience=3, nationalite="Allemande")
        equipe = Equipe.objects.create(id_Eq=3, nom="Test Team", stade="Stade Test", entraineur=entraineur)
        delete_in_base(3, "equipe")
        self.assertEqual(Equipe.objects.filter(id_Eq=3).count(), 0)
