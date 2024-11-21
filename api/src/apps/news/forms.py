from django import forms
from api.src.models.news import Formsnews

class FeedbackCreateForm(forms.ModelForm):
    """
    Форма отправки обратной связи
    """

    class Meta:
        model = Formsnews
        fields = ('nameComm', 'emailComm', 'textComm')
