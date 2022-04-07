from django.shortcuts import render


def error_404(request, exception=None):
    return render(request, '404.html', status=404)


def home(request):
    return render(request, 'home.html')
