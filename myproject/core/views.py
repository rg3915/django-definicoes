from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.views.generic import CreateView
from .models import Person, Book


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


def person_redirected(request, pk):
    person = Person.objects.get(pk=pk)
    return HttpResponse(f'<p>Você foi redirecionado! pk: {pk}</p><p>{ person.name }</p>')


def person_detail(request, pk):
    obj = Person.objects.get(pk=pk)
    print('Você será redirecionado')
    return redirect(obj)


def persons_redirected(request):
    return HttpResponse(f'<p>Você foi redirecionado!</p>')


def persons(request):
    print('Você será redirecionado')
    return redirect('core:persons_redirected')


def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return HttpResponse(f'Book: {book}')


class BookCreateView(CreateView):
    model = Book
    fields = '__all__'
