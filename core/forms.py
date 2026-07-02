from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Honeypot: hidden from humans, bots tend to fill it.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your name",
                "autocomplete": "name",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "you@example.com",
                "autocomplete": "email",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "What are we building?",
                "rows": 5,
            }),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Spam detected.")
        return cleaned
