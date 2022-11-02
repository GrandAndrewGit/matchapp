from django import forms
from .models import DataSet

class DataSetForm(forms.ModelForm):
    class Meta:
        model = DataSet
        fields = ('csv_file', 'xml_file', )
