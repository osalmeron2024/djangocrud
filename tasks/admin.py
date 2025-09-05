"""Importaciones de Modules
"""
from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    """
    Con readonly_fields, estoy configurando que los campos automáticos sean visibles
    desde el Admin Site
    """
    readonly_fields = ('created',)

    # Register your models here.
admin.site.register(Task, TaskAdmin)
