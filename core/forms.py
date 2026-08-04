from django import forms
from .models import Comment, ContactMessage


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ismingiz", "required": True}),
            "email": forms.EmailInput(attrs={"placeholder": "Email (ixtiyoriy)"}),
            "message": forms.Textarea(attrs={"placeholder": "Izohingiz...", "rows": 4}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Ism kiritish majburiy.")
        return name


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "required": True}),
            "email": forms.EmailInput(attrs={"placeholder": "Your email", "required": True}),
            "message": forms.Textarea(attrs={"placeholder": "Tell me about your project...", "rows": 6}),
        }
