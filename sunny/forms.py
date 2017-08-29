from django import forms


class PictureChangeForm(forms.Form):
    picture = forms.ImageField()
