from django import forms

RESEAUX_CHOICES = [
    ('MOOV', 'MOOV'),
    ('MTN', 'MTN'),
]


class InitPaymentForm(forms.Form):
    reseau = forms.ChoiceField(
        choices=RESEAUX_CHOICES,
        label='Réseau',
        required = True
    )

    phone_number = forms.CharField(
        label='Numéro de téléphone',
        max_length=20,
        required=True
    )
