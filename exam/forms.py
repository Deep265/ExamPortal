from django import forms
from .models import Exam

class Examform(forms.ModelForm):
    class Meta:
        model = Exam
        fields =['question','option1','option2','option3','option4','optionimg1','optionimg2','optionimg3','optionimg4','correctimg']
