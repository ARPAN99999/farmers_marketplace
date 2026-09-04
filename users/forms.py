from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    role = forms.ChoiceField(choices=[('consumer', 'Consumer'), ('farmer', 'Farmer')])
    phone = forms.CharField(max_length=20, required=False)
    location = forms.CharField(max_length=120, required=False)
