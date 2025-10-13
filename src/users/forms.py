# Fichier : src/users/forms.py
from django import forms

class UserCreationForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=100)
    email = forms.EmailField(label="Adresse e-mail", required=False)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirmez le mot de passe", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data

class UserEditForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=100)
    email = forms.EmailField(label="Adresse e-mail", required=False)

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Votre adresse e-mail")

class PasswordResetConfirmForm(forms.Form):
    new_password = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmez le nouveau mot de passe", widget=forms.PasswordInput)


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("new_password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data


