"""
Importación de las librerías
from django.contrib.auth.forms import \
    UserCreationForm  # Formulario de login ya construido por django
from django.contrib.auth.models import \
    User  # Modelo o tabla definida por djando para guardar un usuario
from django.http import HttpResponse  # Para enviar respuestas o mensajes
"""
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import Http404
from django.utils import timezone

from .formauth import RegistroForm
from .signin import LoginForm
from .taskform import TaskForm
from .models import Task
import logging

logger = logging.getLogger(__name__)

# pylint: disable=too-many-ancestors


class CustomLoginView(LoginView):
    """
    Vista basada en clase (CBV) con LoginView
    🔹 Ventajas:
        Menos código repetido.
        Puedes sobreescribir métodos como form_valid() para añadir lógica extra
        (por ejemplo, logging de accesos o métricas ejecutivas para tu reporting).
    """
    template_name = "tasks/signin.html"
    authentication_form = LoginForm

    # redirect_authenticated_user = True Si el usuario que llega a esta vista ya
    # está autenticado, no le muestres el     # formulario de login; en su lugar,
    # redirígelo automáticamente a la URL de éxito
    redirect_authenticated_user = True  # Evita que usuarios logueados vean el login

    def get_success_url(self):
        """
        Sobreescribo el metodo get_success_url para que cuando la autenticación
        sea exitosa(User y Pass correctos) lo mande al panel de task
        """
        return reverse_lazy("list_tasks")  # o cualquier ruta


# Create your views here.
def home(request):
    """
    Función que carga página html de home
    """
    return render(request, 'tasks/home.html')


def signup(request):
    """
    Función que carga página html de Signup con un formulario de login
    """
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')  # o a la página que quieras
    else:
        form = RegistroForm()
    return render(request, 'tasks/signup.html', {'form': form})


@login_required
def show_tasks(request):
    """
    Funcion que muestra o enlistas las tareas(Tasks)
    """
    listtask = Task.objects.filter(
        user=request.user, datecompleted__isnull=True
    )
    return render(request, 'tasks/tasks.html', {'tasks': listtask,
                                                'status': 'Pending'})


@login_required
def completed_tasks(request):
    """
    Funcion que muestra o enlistas las tareas(Tasks)
    """
    listtask = Task.objects.filter(
        user=request.user, datecompleted__isnull=False
    ).order_by('-datecompleted')
    return render(request, 'tasks/tasks.html', {'tasks': listtask,
                                                'status': 'Completed'})


@login_required
def create_task(request):

    if request.method == 'POST':
        form = TaskForm(request.POST)
        try:
            if form.is_valid():
                # Aquí ya sabes que el usuario está autenticado
                taskfrom = form.save(commit=False)
                # Se asigna manualmente el usuario autenticado (request.user) al campo user del modelo.
                taskfrom.user = request.user
                taskfrom.save()
                messages.success(
                    request, "✅ La tarea fue creada exitosamente.")
                return redirect('list_tasks')
            else:
                messages.error(
                    request, "❌ El formulario tiene errores. Revisa los campos.")
        except Exception as e:
            messages.error(request, f"⚠️ Ocurrió un error inesperado: {e}")
    else:
        form = TaskForm()
        return render(request, 'tasks/create_task.html', {'form': form})


@login_required
def show_task_detail(request, id_task):

    if request.method == 'GET':
        try:
            # filter_task = get_object_or_404(Task, pk=id_task)
            filter_task = Task.objects.get(pk=id_task, user=request.user)
            form = TaskForm(instance=filter_task)
            return render(request, 'tasks/task_detail.html',
                          {'form': form,
                           'filter_task': filter_task
                           }
                          )
        except Task.DoesNotExist:
            raise Http404(id_task)
    else:
        filter_task = get_object_or_404(Task, pk=id_task, user=request.user)
        form = TaskForm(request.POST, instance=filter_task)
        try:
            if form.is_valid():
                # Aquí ya sabes que el usuario está autenticado
                taskfrom = form.save(commit=False)
                # Se asigna manualmente el usuario autenticado (request.user) al campo user del modelo.
                taskfrom.user = request.user
                taskfrom.save()
                messages.success(
                    request, "✅ La tarea se actualizó exitosamente.")
                return redirect('list_tasks')
            else:
                messages.error(
                    request, "❌ El formulario tiene errores. Revisa los campos.")
        except Exception as e:
            messages.error(request, f"⚠️ Ocurrió un error inesperado: {e}")


@login_required
def complete_task(request, id_task):
    try:
        # filter_task = get_object_or_404(Task, pk=id_task)
        filter_task = get_object_or_404(Task, pk=id_task, user=request.user)
        logger.debug("👉 Método HTTP: %s", request.method)
        if request.method == 'POST':
            logger.debug("👉 Antes de actualizar: %s",
                         filter_task.datecompleted)
            filter_task.datecompleted = timezone.now()
            filter_task.save()
            logger.debug("👉 Después de actualizar: %s",
                         filter_task.datecompleted)
            return redirect('list_tasks')
    except Task.DoesNotExist:
        raise Http404(id_task)


@login_required
def remove_task(request, id_task):
    try:
        # filter_task = get_object_or_404(Task, pk=id_task)
        filter_task = get_object_or_404(Task, pk=id_task, user=request.user)
        if request.method == 'POST':
            filter_task.delete()
            return redirect('list_tasks')
    except Task.DoesNotExist:
        raise Http404(id_task)


@login_required
def close_session(request):
    """
    Función que invoca el metodo logout de django.contrib.auth
    Elimina la sesion guardada en las cookies
    """
    logout(request)
    return redirect('home')
