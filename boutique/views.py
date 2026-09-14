import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Categorie, Produit, Commande, LigneCommande, MessageContact
from .panier import Panier
from .forms import CommandeForm, ContactForm


def accueil(request):
    coups_de_coeur = Produit.objects.filter(disponible=True, coup_de_coeur=True)[:8]
    nouveautes = Produit.objects.filter(disponible=True)[:8]
    categories = Categorie.objects.all()
    return render(request, "boutique/accueil.html", {
        "coups_de_coeur": coups_de_coeur,
        "nouveautes": nouveautes,
        "categories": categories,
    })


def catalogue(request, slug_categorie=None):
    produits = Produit.objects.filter(disponible=True)
    categorie_active = None
    if slug_categorie:
        categorie_active = get_object_or_404(Categorie, slug=slug_categorie)
        produits = produits.filter(categorie=categorie_active)

    recherche = request.GET.get("q", "").strip()
    if recherche:
        produits = produits.filter(Q(nom__icontains=recherche) | Q(description__icontains=recherche))

    tri = request.GET.get("tri", "")
    if tri == "prix_asc":
        produits = produits.order_by("prix")
    elif tri == "prix_desc":
        produits = produits.order_by("-prix")

    categories = Categorie.objects.all()
    return render(request, "boutique/catalogue.html", {
        "produits": produits,
        "categories": categories,
        "categorie_active": categorie_active,
        "recherche": recherche,
        "tri": tri,
    })


def produit_detail(request, slug):
    produit = get_object_or_404(Produit, slug=slug, disponible=True)
    suggestions = Produit.objects.filter(categorie=produit.categorie, disponible=True).exclude(pk=produit.pk)[:4]
    return render(request, "boutique/produit_detail.html", {
        "produit": produit,
        "suggestions": suggestions,
    })


def panier_detail(request):
    panier = Panier(request)
    return render(request, "boutique/panier.html", {"panier": panier})


def panier_ajouter(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id, disponible=True)
    panier = Panier(request)
    quantite = int(request.POST.get("quantite", 1))
    panier.ajouter(produit, quantite=max(1, quantite))
    messages.success(request, f"« {produit.nom} » a été ajouté à votre panier.")
    return redirect(request.POST.get("suivant") or "boutique:panier_detail")


def panier_maj(request, produit_id):
    if request.method == "POST":
        quantite = int(request.POST.get("quantite", 1))
        panier = Panier(request)
        panier.definir_quantite(produit_id, quantite)
    return redirect("boutique:panier_detail")


def panier_retirer(request, produit_id):
    panier = Panier(request)
    panier.retirer(produit_id)
    messages.info(request, "Article retiré du panier.")
    return redirect("boutique:panier_detail")


def commande_creer(request):
    panier = Panier(request)
    if len(panier) == 0:
        messages.warning(request, "Votre panier est vide.")
        return redirect("boutique:catalogue")

    if request.method == "POST":
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save()
            for item in panier:
                LigneCommande.objects.create(
                    commande=commande,
                    produit=item["produit"],
                    nom_produit=item["produit"].nom,
                    prix_unitaire=item["prix"],
                    quantite=item["quantite"],
                )
            panier.vider()
            return redirect("boutique:commande_confirmation", commande_id=commande.id)
    else:
        form = CommandeForm()

    return render(request, "boutique/commande_form.html", {"form": form, "panier": panier})


def commande_confirmation(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, "boutique/commande_confirmation.html", {"commande": commande})


def a_propos(request):
    return render(request, "boutique/a_propos.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre message a bien été envoyé. Nous vous répondrons rapidement, in cha Allah.")
            return redirect("boutique:contact")
    else:
        form = ContactForm()
    return render(request, "boutique/contact.html", {"form": form})


def _donnees_assistant():
    commandes = Commande.objects.all()
    chiffre_affaires = sum((commande.total for commande in commandes if commande.statut != "annulee"), Decimal("0"))
    return {
        "produits": Produit.objects.count(),
        "produits_disponibles": Produit.objects.filter(disponible=True).count(),
        "stock_faible": Produit.objects.filter(disponible=True, stock__lte=3).order_by("stock", "nom")[:5],
        "commandes": commandes.count(),
        "commandes_attente": commandes.filter(statut="en_attente").count(),
        "chiffre_affaires": chiffre_affaires,
        "messages_non_traites": MessageContact.objects.filter(traite=False).count(),
    }


def _reponse_assistant(question):
    question = question.lower().strip()
    donnees = _donnees_assistant()

    if any(mot in question for mot in ["bilan", "résumé", "resume", "situation", "statistique"]):
        return (
            f"Voici le bilan actuel : {donnees['produits']} produits au catalogue, "
            f"dont {donnees['produits_disponibles']} disponibles. "
            f"La boutique compte {donnees['commandes']} commande(s), dont "
            f"{donnees['commandes_attente']} en attente, pour un chiffre d'affaires cumulé de "
            f"{donnees['chiffre_affaires']:,.0f} FCFA hors commandes annulées. "
            f"Il reste {donnees['messages_non_traites']} message(s) client à traiter."
        )

    if any(mot in question for mot in ["stock", "rupture", "inventaire"]):
        produits = list(donnees["stock_faible"])
        if not produits:
            return "Aucun produit disponible n'a un stock inférieur ou égal à 3 unités."
        details = ", ".join(f"{produit.nom} ({produit.stock})" for produit in produits)
        return f"Les stocks à surveiller sont : {details}. Pensez à les réapprovisionner ou à masquer les articles épuisés."

    if any(mot in question for mot in ["commande", "vente", "achat"]):
        return (
            f"Vous avez {donnees['commandes']} commande(s), dont {donnees['commandes_attente']} en attente. "
            "Vous pouvez modifier leur statut depuis la rubrique Commandes de l'administration Django."
        )

    if any(mot in question for mot in ["message", "contact", "client"]):
        return (
            f"Il y a {donnees['messages_non_traites']} message(s) de contact non traité(s). "
            "Ouvrez la rubrique Messages de contact pour les lire et les marquer comme traités."
        )

    if any(mot in question for mot in ["produit", "catalogue", "article"]):
        return (
            f"Le catalogue contient {donnees['produits']} produit(s), dont {donnees['produits_disponibles']} visible(s). "
            "Je peux aussi vous aider à repérer les stocks faibles ou les articles à mettre en avant."
        )

    return (
        "Je peux vous aider à piloter la boutique. Essayez : « Fais-moi un bilan », "
        "« Quels produits ont un stock faible ? », « Combien de commandes sont en attente ? » "
        "ou « Ai-je des messages clients non traités ? »"
    )


@staff_member_required
def assistant_gestion(request):
    donnees = _donnees_assistant()
    return render(request, "boutique/assistant_gestion.html", {"donnees": donnees})


@staff_member_required
def assistant_gestion_api(request):
    if request.method != "POST":
        return JsonResponse({"erreur": "Méthode non autorisée."}, status=405)

    try:
        contenu = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"erreur": "La question envoyée est invalide."}, status=400)

    question = str(contenu.get("question", ""))[:500]
    if not question.strip():
        return JsonResponse({"erreur": "Écrivez une question pour l'assistant."}, status=400)
    return JsonResponse({"reponse": _reponse_assistant(question)})
