from django import forms


class SendImageForm(forms.Form):
    image_path = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*'}))
