from decimal import Decimal
from .models import Produit

SESSION_KEY = "panier"


class Panier:
    """Panier simple stocké dans la session (aucune base de données requise)."""

    def __init__(self, request):
        self.session = request.session
        panier = self.session.get(SESSION_KEY)
        if panier is None:
            panier = self.session[SESSION_KEY] = {}
        self.panier = panier

    def ajouter(self, produit, quantite=1):
        pid = str(produit.id)
        if pid in self.panier:
            self.panier[pid]["quantite"] += quantite
        else:
            self.panier[pid] = {
                "quantite": quantite,
                "prix": str(produit.prix_actuel),
            }
        self.sauvegarder()

    def definir_quantite(self, produit_id, quantite):
        pid = str(produit_id)
        if pid in self.panier:
            if quantite <= 0:
                del self.panier[pid]
            else:
                self.panier[pid]["quantite"] = quantite
            self.sauvegarder()

    def retirer(self, produit_id):
        pid = str(produit_id)
        if pid in self.panier:
            del self.panier[pid]
            self.sauvegarder()

    def vider(self):
        self.session[SESSION_KEY] = {}
        self.sauvegarder()

    def sauvegarder(self):
        self.session.modified = True

    def __len__(self):
        return sum(item["quantite"] for item in self.panier.values())

    def __iter__(self):
        produit_ids = self.panier.keys()
        produits = Produit.objects.filter(id__in=produit_ids)
        produits_dict = {str(p.id): p for p in produits}
        for pid, item in self.panier.items():
            produit = produits_dict.get(pid)
            if not produit:
                continue
            prix = Decimal(item["prix"])
            yield {
                "produit": produit,
                "quantite": item["quantite"],
                "prix": prix,
                "sous_total": prix * item["quantite"],
            }

    @property
    def total(self):
        return sum(Decimal(item["prix"]) * item["quantite"] for item in self.panier.values())
