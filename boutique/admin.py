from django.contrib import admin
from .models import Categorie, Produit, ImageProduit, Commande, LigneCommande, MessageContact


class ImageProduitInline(admin.TabularInline):
    model = ImageProduit
    extra = 1


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ["nom", "ordre"]
    prepopulated_fields = {"slug": ("nom",)}


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ["nom", "categorie", "prix", "prix_promo", "stock", "disponible", "coup_de_coeur"]
    list_filter = ["categorie", "disponible", "coup_de_coeur"]
    search_fields = ["nom", "description"]
    prepopulated_fields = {"slug": ("nom",)}
    inlines = [ImageProduitInline]


class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 0
    readonly_fields = ["produit", "nom_produit", "prix_unitaire", "quantite"]


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ["id", "nom_complet", "telephone", "ville", "statut", "date_creation"]
    list_filter = ["statut", "ville"]
    search_fields = ["nom_complet", "telephone", "email"]
    inlines = [LigneCommandeInline]


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ["nom", "sujet", "email", "date_envoi", "traite"]
    list_filter = ["traite"]

admin.site.site_header = "Habiballah Élégance — Administration"
admin.site.site_title = "Habiballah Élégance"
admin.site.index_title = "Gestion de la boutique"
