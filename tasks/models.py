"""
Importamos las librerías necesarias para la implementacion del mapeo de las
clases con las tablas de BBDD
"""
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    """
    Definicion de los atributos de la clase Task para el mapeo y creacion de
    la tabla en la BBDD
    __str__ returns <type 'str'>
    """
    title = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Esto hace que se muestre el titulo y el usuario de la tarea en el Admin site
        """
        return f'{self.title} - by {self.user.username}'  # pylint: disable=no-member
