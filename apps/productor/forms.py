from django import forms
from .models import EstadoOferta, Oferta


class OfertaForm(forms.ModelForm):

    class Meta:
        """se define de que modelo hereda"""
        model = Oferta
        """se definen los campos"""
        fields = [
            'precio',
            'cantidad',
            'producto',
            'productor',
        ]
        """los labels del formulario a mostrar en pantalla"""
        labels = {
            'precio': 'Precio',
            'cantidad': 'Cantidad',
            'producto': 'Producto',
            'productor': 'Productor',
        }
        widgets = {
            'precio': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'productor': forms.Select(attrs={'class': 'form-control'}),
        }