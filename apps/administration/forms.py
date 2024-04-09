from django import forms

from apps.administration.models import Investimento

class InvestimentoForm(forms.ModelForm):
    class Meta:
        model = Investimento
        fields = (
            'obs',
        )
    
