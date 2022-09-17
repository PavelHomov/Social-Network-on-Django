from django.shortcuts import render
from http.client import FORBIDDEN, INTERNAL_SERVER_ERROR, NOT_FOUND


def page_not_found(request, exception):
    return render(request, 'core/404.html', {'path': request.path}, status=NOT_FOUND)


def csrf_failure(request, exception):
    return render(request, 'core/403csrf.html', status=FORBIDDEN)


def server_error(request):
    return render(request, 'core/500.html', status=INTERNAL_SERVER_ERROR)
