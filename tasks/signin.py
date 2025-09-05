"""
Importamos las librerías que se usaremos
En Django, el punto de partida es AuthenticationForm de django.contrib.auth.forms,
pero como no es un ModelForm sino un Form normal, lo habitual es heredarlo y 
sobreescribir lo que necesites.

- get_user_model()
En Django, la función get_user_model() devuelve la clase del modelo de usuario activo
en tu proyecto.

Por defecto, Django trae el modelo User que vive en django.contrib.auth.models.
Pero si tú configuraste un modelo de usuario personalizado en settings.py con:
AUTH_USER_MODEL = 'mi_app.MiUsuario'

get_user_model() es la forma recomendada en Django de obtener el modelo de usuario, 
porque se adapta tanto al modelo por defecto como a modelos personalizados.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class LoginForm(AuthenticationForm):
    """
    Clase que tiene la logica para la auticación de un usuario que esta de alta
    en la BBDD.
    """
    username = forms.CharField(
        # Se usa _() porque generalmente está asociado a la función de traducción de
        # Django (gettext_lazy), lo que permite que "Contraseña" pueda mostrarse en
        # diferentes idiomas si usas internacionalización (i18n).
        label=_("Usuario o correo"),
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ingresa tu usuario o email"
        })
    )
    password = forms.CharField(
        label=_("Contraseña"),
        # Indica que Django no eliminará espacios en blanco al inicio o al final
        # del valor ingresado.
        # Por defecto CharField hace strip=True, pero aquí se desactiva porque una
        # contraseña podría tener espacios válidos.
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Ingresa tu contraseña"
        })
    )

    error_messages = {  # error_messages: personaliza los mensajes de error.
        "invalid_login": _(
            "Por favor verifica tu usuario y contraseña. "
            "Recuerda que ambos campos pueden ser sensibles a mayúsculas."
        ),
        "inactive": _("Esta cuenta está inactiva."),
    }

    def confirm_login_allowed(self, user):
        """
        hook para validar condiciones extra antes de permitir el login.
        Método que se ejecuta después de validar credenciales,
        antes de iniciar sesión.
        Aquí puedes poner reglas adicionales.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )
        # Ejemplo: bloquear usuarios con flag personalizado
        if hasattr(user, "bloqueado") and user.bloqueado:
            raise forms.ValidationError(
                _("Tu cuenta está bloqueada, contacta soporte."),
                code="blocked",
            )
