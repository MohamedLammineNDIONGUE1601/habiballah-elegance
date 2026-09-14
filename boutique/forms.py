from django import forms
from .models import Commande, MessageContact


class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ["nom_complet", "telephone", "email", "adresse_livraison", "ville", "note"]
        widgets = {
            "nom_complet": forms.TextInput(attrs={"placeholder": "Votre nom complet"}),
            "telephone": forms.TextInput(attrs={"placeholder": "+221 77 000 00 00"}),
            "email": forms.EmailInput(attrs={"placeholder": "vous@exemple.com (optionnel)"}),
            "adresse_livraison": forms.Textarea(attrs={"rows": 3, "placeholder": "Quartier, ville, point de repère..."}),
            "ville": forms.TextInput(attrs={"placeholder": "Matam"}),
            "note": forms.Textarea(attrs={"rows": 2, "placeholder": "Instructions particulières (optionnel)"}),
        }
        labels = {
            "nom_complet": "Nom complet",
            "telephone": "Téléphone",
            "email": "Email",
            "adresse_livraison": "Adresse de livraison",
            "ville": "Ville",
            "note": "Note",
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = MessageContact
        fields = ["nom", "email", "telephone", "sujet", "message"]
        widgets = {
            "nom": forms.TextInput(attrs={"placeholder": "Votre nom"}),
            "email": forms.EmailInput(attrs={"placeholder": "vous@exemple.com"}),
            "telephone": forms.TextInput(attrs={"placeholder": "+221 77 000 00 00"}),
            "sujet": forms.TextInput(attrs={"placeholder": "Sujet"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "Votre message..."}),
        }
