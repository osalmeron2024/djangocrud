"""
Importamos las librerías que se usaremos
"""
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistroForm(forms.ModelForm):
    """
    Clase RegistroForm, validar si el usuario ya existe en la BBDD
    """
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            'placeholder': 'Ingrese Contraseña'})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                'placeholder': 'Confirme Contraseña'})
    )
    username = forms.CharField(
        label='Nombre Usuario',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            'placeholder': 'Ingrese el Usuario'})
    )

    email = forms.CharField(
        label='Correo Electrónico',
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                'placeholder': 'Escriba su correo ejemplo@gmail.com'})
    )

    class Meta:
        """
        Meta le dice a Django qué modelo usar y qué campos incluir
        automáticamente en el formulario(User)

        fields = ['username', 'email'] → solo incluirá estos campos del
        modelo, además de los que tú definas manualmente (password1, password2).
        """
        model = User
        # Django te construye un formulario con <input> para username y email,
        # ligados al modelo User
        fields = ['username', 'email']

    def clean_username(self):
        """
        Sobreescribimos el metodo clean_username para validar si el usuario existe en BBDD
        En Django, cualquier método con el nombre clean_<campo> sirve para validar un campo e
        specífico de un formulario.

        self.cleaned_data es un diccionario que contiene los valores del formulario después 
        de pasar las validaciones básicas (tipos de datos, campos requeridos, etc.).
        Aquí se extrae el valor que el usuario escribió en el campo username.
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError(f'Username << {username} >> already exists!')
        return username

    def clean(self):
        """
        En los formularios de Django, el método clean() se usa para realizar 
        validaciones que involucran múltiples campos al mismo tiempo.
        Llama al clean() de la clase padre (forms.ModelForm) para obtener 
        todos los datos ya validados previamente (tipo de dato, requeridos, etc.).

        El resultado es un diccionario con los datos limpios del formulario,
        por ejemplo:
                {
            'username': 'juanito',
            'email': 'juan@mail.com',
            'password1': 'abc123',
            'password2': 'abc123'
        }
        Usa .get() para evitar errores si alguna de las llaves no existe
        (retorna None en ese caso).

        return cleaned_data
        Si no hubo problemas, retorna todos los datos validados para que 
        Django continúe con el flujo normal (guardar el usuario, etc.).
        """
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            # Se interrumpe el flujo, no llego al return
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        """
        def save(self, commit=True):
        Es un método sobrescrito del ModelForm.
        Django permite redefinir save() para personalizar cómo se guardan los datos del modelo.
        El parámetro commit=True indica si debe guardar inmediatamente en la base de datos o no.

        user = super().save(commit=False)
        Llama al save() original de ModelForm, pero con commit=False.
        Esto crea una instancia del modelo User en memoria, con los datos del formulario 
        (username, email), pero no lo guarda aún en la base de datos.

        user.set_password(self.cleaned_data["password1"])
        Convierte la contraseña en un hash seguro usando el sistema de Django.
        Nunca guarda la contraseña en texto plano.

        if commit: user.save()
        Si commit=True (valor por defecto): guarda el usuario en la base de datos.
        Si commit=False: devuelve el objeto user sin guardarlo (útil si quieres hacer
        más cambios antes de persistirlo).

        return user
        Retorna la instancia del User.
        Así el código que llama al formulario puede seguir trabajando con el usuario
        creado (guardado o no, según commit).
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
