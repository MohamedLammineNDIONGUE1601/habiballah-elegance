from django.urls import path
from . import views

app_name = "boutique"

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("assistant-gestion/", views.assistant_gestion, name="assistant_gestion"),
    path("assistant-gestion/api/", views.assistant_gestion_api, name="assistant_gestion_api"),
    path("boutique/", views.catalogue, name="catalogue"),
    path("boutique/categorie/<slug:slug_categorie>/", views.catalogue, name="categorie_detail"),
    path("produit/<slug:slug>/", views.produit_detail, name="produit_detail"),

    path("panier/", views.panier_detail, name="panier_detail"),
    path("panier/ajouter/<int:produit_id>/", views.panier_ajouter, name="panier_ajouter"),
    path("panier/maj/<int:produit_id>/", views.panier_maj, name="panier_maj"),
    path("panier/retirer/<int:produit_id>/", views.panier_retirer, name="panier_retirer"),

    path("commande/", views.commande_creer, name="commande_creer"),
    path("commande/confirmation/<int:commande_id>/", views.commande_confirmation, name="commande_confirmation"),

    path("a-propos/", views.a_propos, name="a_propos"),
    path("contact/", views.contact, name="contact"),
]
