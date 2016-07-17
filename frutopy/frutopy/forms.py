from django import forms
from models import Sample

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class ValidateForm(forms.ModelForm):
    label_is_right = forms.BooleanField()

    class Meta:
        model = Sample