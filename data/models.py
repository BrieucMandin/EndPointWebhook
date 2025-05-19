from django.db import models


class Joueur(models.Model):

    POSTE_CHOICES = [
        ("GK", "Gardien"),
        ("DEF", "Défenseur"),
        ("MID", "Milieu"),
        ("ATT", "Attaquant"),
    ]

    PIED_FORT_CHOICES = [("D", "Droit"), ("G", "Gauche"), ("O", "Ousmane Dembélé")]

    id_J = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100)
    age = models.IntegerField()
    poste = models.CharField(
        max_length=3,
        choices=POSTE_CHOICES,  # Appliquer les choix possibles
        default="MID",  # Valeur par défaut
    )
    nationalite = models.CharField(max_length=50)
    pied_fort = models.CharField(max_length=1, choices=PIED_FORT_CHOICES, default="D")
    nombre_but = models.IntegerField()

    def __str__(self):
        return f"{self.nom} ({self.poste})"


class Entraineur(models.Model):
    id_En = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100)
    experience = models.IntegerField(help_text="Années d'expérience")
    nationalite = models.CharField(max_length=50)

    def __str__(self):
        return self.nom


class Equipe(models.Model):
    id_Eq = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100)
    stade = models.CharField(max_length=100)
    entraineur = models.OneToOneField(Entraineur, on_delete=models.CASCADE)
    joueurs = models.ManyToManyField(Joueur)

    def __str__(self):
        return self.nom
