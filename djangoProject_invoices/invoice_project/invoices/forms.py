from django import forms
from django_select2.forms import Select2Widget
from dal import autocomplete
from .models import Invoice, GeneratedInvoice, InvoiceWorkItem
import datetime
from django.forms import inlineformset_factory


class InvoiceForm(forms.ModelForm):
    pdf_file = forms.FileField(required=False, label='Įkelti naują PDF failą')

    class Meta:
        model = Invoice
        fields = ['projekto_nr', 'tiekejas', 'saskaitos_nr', 'israsymo_data', 'apmoketi_iki', 'apmokejimo_data',
                  'apmoketa_ne', 'skubu', 'pastabos', 'pdf_path', 'suma_be_pvm']
        widgets = {
            'projekto_nr': forms.TextInput(attrs={'id': 'id_projekto_nr', 'class': 'select2', 'style': 'width: 250px;'}),
            'tiekejas': forms.TextInput(attrs={'id': 'id_tiekejas', 'class': 'select2', 'style': 'width: 250px;'}),
            'saskaitos_nr': forms.TextInput(attrs={'style': 'width: 200px;'}),
            'israsymo_data': forms.DateInput(attrs={'type': 'date', 'style': 'width: 200px;'}),
            'apmoketi_iki': forms.DateInput(attrs={'type': 'date', 'style': 'width: 200px;'}),
            'apmokejimo_data': forms.DateInput(attrs={'type': 'date', 'style': 'width: 200px;'}),
            'apmoketa_ne': forms.CheckboxInput(attrs={'style': 'margin-left: 10px;'}),
            'skubu': forms.CheckboxInput(attrs={'style': 'margin-left: 10px'}),
            'pastabos': forms.TextInput(attrs={'style': 'width: 235px; height: 50px;'}),
            # 'pdf_path': forms.ClearableFileInput(attrs={'style': 'width: 200px;'}),
            'pdf_path': forms.HiddenInput(),  # įrašomas tik kaip UR po įkėlimo
            'suma_be_pvm': forms.NumberInput(attrs={'style': 'width: 200px;'})
        }

        labels = {
            'projekto_nr': 'Projekto Nr.',
            'tiekejas': 'Tiekėjas',
            'saskaitos_nr': 'Sąskaitos Nr.',
            'israsymo_data': 'Išrašymo data',
            'apmoketi_iki': 'Apmokėti iki',
            'apmokejimo_data': 'Apmokėjimo data',
            'apmoketa_ne': 'Apmokėta',
            'skubu': 'Skubu',
            'pastabos': 'Pastabos',
            'pdf_path': 'PDF failas',
            'suma_be_pvm': 'Suma (be PVM)'
        }


class InvoiceFilterForm(forms.Form):
    # projekto_nr = forms.CharField(label='Projekto Nr.', max_length=100, required=False, widget=Select2Widget)
    projekto_nr = forms.CharField(label='Projekto Nr.', max_length=100, required=False, widget=autocomplete.Select2(url='filter_projects', attrs={'style': 'width: 250px;'}))
    # tiekejas = forms.CharField(label='Tiekėjas', max_length=100, required=False, widget=Select2Widget)
    tiekejas = forms.CharField(label='Tiekėjas', max_length=100, required=False, widget=autocomplete.Select2(url='filter_suppliers', attrs={'style': 'width: 250px;'}))

    current_year = datetime.datetime.now().year
    year_choices = [(year, year) for year in range(current_year, current_year - 5, -1)]
    metai = forms.ChoiceField(label='Metai', choices=year_choices, required=False)

    ketvirtis = forms.ChoiceField(label='Ketvirtis', choices=[
            ('', 'Visi'), ('1', 'Pirmas'), ('2', 'Antras'), ('3', 'Trečias'), ('4', 'Ketvirtas')], required=False)
    menuo = forms.ChoiceField(label='Menuo', choices=[
            ('', 'Visi'), ('1', 'Sausis'), ('2', 'Vasaris'), ('3', 'Kovas'), ('4', 'Balandis'),
        ('5', 'Gegužė'), ('6', 'Birželis'), ('7', 'Liepa'), ('8', 'Rugpjūtis'),
        ('9', 'Rugsėjis'), ('10', 'Spalis'), ('11', 'Lapkritis'), ('12', 'Gruodis')], required=False)


###################   SĄSKAITŲ IŠRAŠYMAS   #######################


class GeneratedInvoiceForm(forms.ModelForm):
    class Meta:
        model = GeneratedInvoice
        fields = ['saskaitos_numeris', 'projekto_nr', 'pirkejas', 'imones_kodas', 'PVM_kodas', 'pirkejo_adresas', 'dok_data',
                  'apmoketi_iki', 'israse', 'suma_viso', 'pvm', 'suma_su_pvm']

class InvoiceWorkItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceWorkItem
        fields = ["description", "unit", "quantity", "unit_price", "total_price"]


# sukuriamas FormSet, leidžiantis redaguoti 'InvoiceWorkItem' įrašus, susijusius su 'GeneratedInvoice'
InvoiceWorkItemFormSet = forms.inlineformset_factory(GeneratedInvoice, InvoiceWorkItem, form=InvoiceWorkItemForm,
                                                     fields=('description', 'unit', 'quantity', 'unit_price', 'total_price'),
                                                     extra=1, can_delete=True)
