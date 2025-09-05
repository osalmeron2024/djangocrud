from django.shortcuts import render

# Create your views here.


def custom_page_not_found(request, exception):
    return render(
        request,
        'customerrors/404.html',
        {
            "status_code": 404,
            "title": f"Tarea con ID: {exception} no encontrada",
            "mensaje": "La tarea solicitada no existe o fue eliminada.",
            'small_title': 'Tarea'
        },
        status=404
    )


def custom_server_error(request):
    return render(request, 'customerrors/500.html', status=500)
