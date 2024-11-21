from django import forms
from src.models.settings import FormsHome

class formsHome(forms.ModelForm):
    class Meta:
        model = FormsHome
        fields = ['nameFormsHome', 'emailFormsHome', 'callFormsHome', 'massageFormsHome']