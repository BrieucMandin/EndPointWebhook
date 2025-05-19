from django.contrib import admin

from .models import Joueur, Entraineur, Equipe


# Personnalisation de l'affichage du modèle Joueur
class JoueurAdmin(admin.ModelAdmin):
    list_display = ("nom", "age", "poste", "nationalite", "pied_fort", "nombre_but")  # Champs à afficher dans la liste
    search_fields = ("nom", "poste", "nationalite")  # Champs qui peuvent être recherchés
    list_filter = ("poste", "pied_fort")  # Filtres à gauche dans l'interface


# Personnalisation de l'affichage du modèle Entraineur
class EntraineurAdmin(admin.ModelAdmin):
    list_display = ("nom", "experience", "nationalite")  # Champs à afficher dans la liste
    search_fields = ("nom", "nationalite")  # Champs qui peuvent être recherchés


# Personnalisation de l'affichage du modèle Equipe
class EquipeAdmin(admin.ModelAdmin):
    list_display = ("nom", "stade", "entraineur", "joueurs_list")  # Champs à afficher dans la liste
    search_fields = ("nom", "stade")  # Champs qui peuvent être recherchés

    # Méthode pour afficher les noms des joueurs dans la liste des équipes
    def joueurs_list(self, obj):
        return ", ".join([joueur.nom for joueur in obj.joueurs.all()])

    joueurs_list.short_description = "Joueurs"  # Nom de la colonne dans l'admin


# Enregistrement des modèles dans l'admin
admin.site.register(Joueur, JoueurAdmin)
admin.site.register(Entraineur, EntraineurAdmin)
admin.site.register(Equipe, EquipeAdmin)
