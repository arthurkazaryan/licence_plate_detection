from django import forms


class SendTextForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'input-form form-middle',
                                                                         'autofocus': True}))
