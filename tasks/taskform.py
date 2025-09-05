"""
Importacion de modulos
"""
from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """
    Con clean_<campo>, por ejemplo, clean_email(self), puede validar el email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and email.endswith('@gmail.com'):
            raise ValidationError("No se permiten correos genéricos para clientes corporativos.")
        return email

    🔍 ¿Qué puedes validar con clean_<campo>?
        Formato personalizado (ej. prefijos, sufijos, longitud)
        Restricciones de negocio (ej. dominio, rango, unicidad condicional)
        Coherencia con otros campos (ej. fecha de nacimiento vs edad mínima)
        Preparación para empaquetado (ej. normalizar valores antes de exportar)
    """
    title = forms.CharField(
        label="Titulo",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            'placeholder': 'Ingrese Titulo'}
        )
    )
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                'placeholder': 'Ingrese Descripción'}
        )
    )

    important = forms.BooleanField(required=False,
                                   label="Importante",
                                   widget=forms.CheckboxInput(
                                       attrs={
                                           "class": "form-check-input"}
                                   )
                                   )

    class Meta:
        model = Task
        fields = ['title', 'descripcion', 'important']
