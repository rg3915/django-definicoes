from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

rendered = render_to_string('my_template.html', {'name': 'render_to_string'})


def my_http_response(request):
    return HttpResponse(rendered)


def my_render_to_response(request):
    return render_to_response('my_template.html', {'name': 'render_to_response'})


def users(request):
    return HttpResponse('<h1>Users</h1>')


def user_detail(request, pk):
    return HttpResponse(f'User {pk}')


def ping(request):
    print(request.GET)
    name = request.GET.get('name')
    return HttpResponse(f'pong {name}')


def index(request):
    template_name = 'index.html'
    return render(request, template_name)
