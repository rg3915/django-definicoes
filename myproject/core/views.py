from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .forms import BookForm
from .models import Person, Book


rendered = render_to_string('my_template.html', {'name': 'render_to_string'})


def my_http_response(request):
    return HttpResponse(rendered)


def my_render_to_response(request):
    return render_to_response('my_template.html', {'name': 'render_to_response'})


@login_required(login_url=reverse_lazy('admin:login'))
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


class BookListView(ListView):
    model = Book


def book_create(request):
    form = BookForm(request.POST or None)
    template_name = 'core/book_add.html'

    if request.method == 'POST':
        ...
        if form.is_valid():
            ...
            new_obj = form.save()
            # kw = {'pk': new_obj.pk}
            # return HttpResponseRedirect(reverse('core:person_detail', kwargs=kw))
            return redirect('core:book_detail', new_obj.pk)
        msg_error = form.errors.get('title')[0]
        messages.error(request, msg_error)
        return redirect('core:book_list')

    context = {'form': form}
    return render(request, template_name, context)


class BookCreateView(CreateView):
    model = Book
    fields = '__all__'
    # Se quiser ir direto para o objeto criado então use get_absolute_url.
    # O reverse vai dar erro.
    # success_url = reverse_lazy('core:book_list')

    def get_success_url(self):
        # Se não quiser usar o get_absolute_url e quiser passar
        # a instância criada para redirecionar manualmente...
        return reverse_lazy('core:book_detail', kwargs={'pk': self.object.pk})
        # ou
        # return reverse_lazy('core:book_detail', args=(self.object.pk,))


def book_redirected(request):
    return HttpResponseRedirect(reverse('core:book_list'))


# def ping_json(request):
#     name = request.GET.get('name')
#     age = request.GET.get('age')
#     data = {
#         'name': name,
#         'age': age
#     }
#     return JsonResponse(data)


def ping_json(request):
    name = request.GET.get('name')
    age = request.GET.get('age')
    data = {}
    if name:
        data['name'] = name
    if age:
        data['age'] = age
    return JsonResponse(data)
