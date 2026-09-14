from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Categorie(models.Model):
    nom = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["ordre", "nom"]

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("boutique:categorie_detail", args=[self.slug])


class Produit(models.Model):
    nom = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    categorie = models.ForeignKey(Categorie, related_name="produits", on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    matiere = models.CharField("Matière / tissu", max_length=150, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=0, help_text="Prix en FCFA")
    prix_promo = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, help_text="Prix promotionnel en FCFA (optionnel)")
    image_principale = models.ImageField(upload_to="produits/", blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    coup_de_coeur = models.BooleanField("Coup de cœur", default=False, help_text="Mettre en avant sur la page d'accueil")
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["-date_ajout"]

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.nom)
            slug = base
            i = 1
            while Produit.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("boutique:produit_detail", args=[self.slug])

    @property
    def prix_actuel(self):
        return self.prix_promo if self.prix_promo else self.prix

    @property
    def en_promo(self):
        return bool(self.prix_promo and self.prix_promo < self.prix)


class ImageProduit(models.Model):
    produit = models.ForeignKey(Produit, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="produits/galerie/")
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordre"]
        verbose_name = "Image supplémentaire"
        verbose_name_plural = "Images supplémentaires"

    def __str__(self):
        return f"Image de {self.produit.nom}"


class Commande(models.Model):
    STATUT_CHOICES = [
        ("en_attente", "En attente"),
        ("confirmee", "Confirmée"),
        ("expediee", "Expédiée"),
        ("livree", "Livrée"),
        ("annulee", "Annulée"),
    ]

    nom_complet = models.CharField(max_length=200)
    telephone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    adresse_livraison = models.TextField()
    ville = models.CharField(max_length=100, default="Matam")
    note = models.TextField(blank=True, help_text="Instructions particulières")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="en_attente")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-date_creation"]

    def __str__(self):
        return f"Commande #{self.pk} — {self.nom_complet}"

    @property
    def total(self):
        return sum(item.sous_total for item in self.lignes.all())


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, related_name="lignes", on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, related_name="lignes_commande", on_delete=models.SET_NULL, null=True)
    nom_produit = models.CharField(max_length=200)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=0)
    quantite = models.PositiveIntegerField(default=1)

    @property
    def sous_total(self):
        return self.prix_unitaire * self.quantite

    def __str__(self):
        return f"{self.quantite} x {self.nom_produit}"


class MessageContact(models.Model):
    nom = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    sujet = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ["-date_envoi"]

    def __str__(self):
        return f"{self.nom} — {self.sujet or 'sans sujet'}"
