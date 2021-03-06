# Passo a passo

Veremos passo a passo como foi construido o projeto.

> Todas as definições estão no [README](README.md) do projeto.

## Criar o projeto inicial

```
git clone https://gist.github.com/b363f5c4a998f42901705b23ccf4b8e8.git /tmp/boilerplatesimple
ls /tmp/boilerplatesimple
cp /tmp/boilerplatesimple/boilerplatesimple.sh .
source boilerplatesimple.sh
# Após terminar de instalar delete o arquivo boilerplatesimple.sh
rm -f boilerplatesimple.sh
```

## Configurar settings.py

```python
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'
```


## Criar um modelo para exemplificar

```python
# models.py
from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'pessoa'
        verbose_name_plural = 'pessoas'

    def __str__(self):
        return self.name
```

## render_to_string

Primeiro vamos criar um template

```
mkdir myproject/core/templates
echo '<p>{{ name }}</p>' > myproject/core/templates/my_template.html
```


Depois, abra o terminal e digite

`./manage.py shell_plus`

depois escreva

```python
from django.template.loader import render_to_string

rendered = render_to_string('my_template.html', {'name': 'render_to_string'})
rendered
```

Então, em `views.py` escreva

```python
# views.py
from django.http import HttpResponse
from django.template.loader import render_to_string

rendered = render_to_string('my_template.html', {'name': 'render_to_string'})


def my_http_response(request):
    return HttpResponse(rendered)
```

E em `urls.py` escreva

```python
# urls.py
from django.urls import path
from myproject.core import views as v


app_name = 'core'


urlpatterns = [
    path('my_http_response/', v.my_http_response, name='my_http_response'),
]
```


Rodando a aplicação, acesse `/my_http_response/`


**Exemplo:** Aliás, um bom exemplo de uso é a preparação de mensagem para envio de e-mail.


## render_to_response

E em `urls.py` escreva

```python
# urls.py
path('my_render_to_response/', v.my_render_to_response, name='my_render_to_response'),
```

E em `views.py` escreva

```python
# views.py
from django.shortcuts import render_to_response


def my_render_to_response(request):
    return render_to_response('my_template.html', {'name': 'render_to_response'})
```

Rodando a aplicação, acesse `/my_render_to_response/`


## HttpResponse

E em `urls.py` escreva

```python
# urls.py
path('user/', v.users, name='users'),
path('user/<int:pk>/', v.user_detail, name='user_detail'),
```

E em `views.py` escreva

```python
# views.py
from django.http import HttpResponse


def users(request):
    return HttpResponse('<h1>Users</h1>')

def user_detail(request, pk):
    return HttpResponse(f'User {pk}')
```


**Exemplo:**

```python
# urls.py
path('ping/', v.ping, name='ping'),
```


```python
# views.py
def ping(request):
    print(request.GET)
    name = request.GET.get('name')
    return HttpResponse(f'pong {name}')
```

Rode a aplicação num terminal, e em outro terminal digite

```python
$ python
>>> import requests
>>> url = 'http://localhost:8000/ping/?name=John&age=42'
>>> r = requests.get(url)
>>> r.content
b'pong John'
```

Veja a saída do print:

`<QueryDict: {'name': ['John'], 'age': ['42']}>`


## render

Crie um novo template

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="shortcut icon" href="https://www.djangoproject.com/favicon.ico">
  <title>Django Definições</title>
  <!-- Bootstrap core CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
</head>
<body>
  <div class="jumbotron">
    <h1>Django Definições</h1>
  </div>

  <ul>
    <li>
      <a href="{% url 'core:my_render_to_response' %}">render_to_response</a>
    </li>
    <li>
      <a href="{% url 'core:my_http_response' %}">http_response</a>
    </li>
    <li>
      <a href="{% url 'core:users' %}">users</a>
    </li>
    <li>
      <a href="{% url 'core:user_detail' 1 %}">user_detail</a>
    </li>
    <li>
      <a href="{ url 'core:person_redirected' 1 %}">person_redirected</a>
    </li>
    <li>
      <a href="{ url 'core:persons' %}">persons</a>
    </li>
    <li>
      <a href="{ url 'core:persons_redirected' %}">persons_redirected</a>
    </li>
    <li>
      <a href="{ url 'core:user_redirected' 1 %}">user_redirected</a>
    </li>
  </ul>
</body>
</html>
```

E em `urls.py` escreva

```python
# urls.py
path('', v.index, name='index'),
```

E em `views.py` escreva

```python
# views.py
from django.shortcuts import render


def index(request):
    template_name = 'index.html'
    return render(request, template_name)
```


## redirected

### Um modelo

Em `models.py` escreva

```python
# models.py
from django.urls import reverse_lazy

class Person(models.Model):
    ...

    def get_absolute_url(self):
        return reverse_lazy('core:person_redirected', kwargs={'pk': self.pk})
```

E em `urls.py` escreva

```python
# urls.py
path('person/<int:pk>/', v.person_detail, name='person_detail'),
path('person/redirected/<int:pk>/', v.person_redirected, name='person_redirected'),
```

E em `views.py` escreva

```python
# views.py
from django.shortcuts import redirect
from .models import Person


def person_redirected(request, pk):
    person = Person.objects.get(pk=pk)
    return HttpResponse(f'<p>Você foi redirecionado! pk: {pk}</p><p>{ person.name }</p>')


def person_detail(request, pk):
    obj = Person.objects.get(pk=pk)
    print('Você será redirecionado')
    return redirect(obj)
```

E em `index.html` escreva

```html
<!-- index.html -->
    <li>
      <a href="{% url 'core:person_detail' 1 %}">person detail</a>
    </li>
```

E em `admin.py` escreva

```python
# admin.py
from django.contrib import admin
from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('name',)
```

### Um nome de view


E em `urls.py` escreva

```python
#urls.py
path('person/', v.persons, name='persons'),
path('person/redirected/', v.persons_redirected, name='persons_redirected'),
```


E em `views.py` escreva

```python
# views.py
def persons_redirected(request):
    return HttpResponse(f'<p>Você foi redirecionado!</p>')


def persons(request):
    print('Você será redirecionado')
    return redirect('core:persons_redirected')
```

E em `index.html` escreva

```html
<!-- index.html -->
<li>
  <a href="{% url 'core:persons' %}">persons</a>
</li>
```

### Uma url absoluta ou relativa, quando for redirecionado pra outro local.

```python
# views.py
def persons(request):
    print('Você será redirecionado')
    return redirect('/person/redirected/')
```

Cuidado, caso você tenha urls parecidas em apps diferentes.


### Passando argumentos


```python
# urls.py
path('user/redirected/<int:pk>/', v.user_redirected, name='user_redirected'),
```


```python
# views.py
def user_redirected(request, pk):
    print('Você será redirecionado para user_detail')
    return redirect('core:user_detail', pk=pk)
```

Leia também [gist: Métodos funções para salvar o form com redirect HttpResponseRedirect](https://gist.github.com/rg3915/27ecf311cc00a47d8fa262e1669e0299).

Veremos um pouco mais de `redirect` mais pra frente.


## reverse

```python
# shell_plus
from django.urls import reverse
>>> reverse('core:users')
'/user/'

reverse('core:user_detail', kwargs={'pk': 1})
'/user/1/'
```

## reverse_lazy

Em `models.py` escreva

```python
# models.py
class Book(models.Model):
    title = models.CharField('título', max_length=50, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'livro'
        verbose_name_plural = 'livros'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('core:book_detail', kwargs={'pk': self.pk})
```

E em `urls.py` escreva

```python
# urls.py
path('book/', v.BookListView.as_view(), name='book_list'),
path('book/<int:pk>/', v.book_detail, name='book_detail'),
path('book/add/', v.BookCreateView.as_view(), name='book_create'),
```



E em `views.py` escreva

```python
# views.py
from django.views.generic import CreateView, ListView

def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return HttpResponse(f'Book: {book}')


class BookListView(ListView):
    model = Book


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
```

Vamos criar o template

```
mkdir myproject/core/templates/core
touch myproject/core/templates/core/book_form.html
touch myproject/core/templates/core/book_list.html
```

```html
<!-- book_form.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="shortcut icon" href="https://www.djangoproject.com/favicon.ico">
  <title>Definitions</title>

  <!-- Bootstrap core CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">

  <style>
    body {
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <form action="." method="POST">
      {% csrf_token %}
      {{ form }}
      <button class="btn btn-primary" type="submit">Salvar</button>
    </form>
  </div>
</body>
</html>
```

```html
<!-- book_list.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="shortcut icon" href="https://www.djangoproject.com/favicon.ico">
  <title>Definitions</title>

  <!-- Bootstrap core CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">

  <style>
    body {
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <ul>
      {% for person in object_list %}
        <li>{{ person }}</li>
      {% endfor %}
    </ul>
  </div>
</body>
</html>
```


```html
<!-- index.html -->
<li>
  <a href="{% url 'core:book_list' %}">book_list</a>
</li>
<li>
  <a href="{% url 'core:book_create' %}">book_create</a>
</li>
```

Usando com o `login_url`


```python
# views.py
from django.contrib.auth.decorators import login_required


@login_required(login_url=reverse_lazy('admin:login'))
def users(request):
    return HttpResponse('<h1>Users</h1>')
```


## Um pouco mais de redirect

Criar `forms.py`

```python
# forms.py
from django import forms
from .models import Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'
```

Criar `templates/core/book_add.html`

```html
<!-- book_add.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="shortcut icon" href="https://www.djangoproject.com/favicon.ico">
  <title>Definitions</title>

  <!-- Bootstrap core CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">

  <style>
    body {
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <form action="." method="POST">
      {% csrf_token %}

      <label for="id_title">Título:</label>
      <input type="text" name="title" maxlength="60" required="" id="id_title">

      <button class="btn btn-primary" type="submit">Salvar</button>
    </form>
  </div>
</body>
</html>
```

Em `index.html`

```html
<li>
  <a href="{% url 'core:book_create' %}">book_create</a>
</li>
<li>
  <a href="{% url 'core:book_create2' %}">book_create2</a>
</li>
```

Em `book_list.html` acrescente dentro de `<body>`

```html
<div class="container">
    {% for message in messages %}
      {% if 'success' in message.tags %}
      <p class="alert alert-success" role="alert"><span style="font-weight:bold">{{ message }}</span></p>
      {% else %}
      <p class="alert alert-danger" role="alert"><span style="font-weight:bold">{{ message }}</span></p>
      {% endif %}
    {% endfor %}

    <ul>
      {% for person in object_list %}
        <li>{{ person }}</li>
      {% endfor %}
    </ul>
  </div>

<!-- jQuery -->
<script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>

<script>
  //close alert after 3 seconds
  window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
      $(this).remove();
    });
  }, 3000);
</script>
```

Em `urls.py`

```python
# urls.py
path('book/add/', v.book_create, name='book_create'),
path('book/add2/', v.BookCreateView.as_view(), name='book_create2'),
```

E finalmente, em `views.py`

```python
# views.py
from django.contrib import messages
...
from .forms import BookForm


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
```


## HttpRequest

**Exemplo:**

Considere

```python
# urls.py
path('ping/', v.ping, name='ping'),
```

```python
# views.py
def ping(request):
    import ipdb
    ipdb.set_trace()
    return HttpResponse('pong')
```

Rode a aplicação, e em outro terminal faça

```python
$ python
>>> import requests
>>> url = 'http://localhost:8000/ping/?name=John&age=42'
>>> result = requests.get(url)
```

No outro terminal o ipdb vai parar antes de retornar a resposta da requisição.

Dai faça

```python
ipdb> request.  # e pressione TAB
```

Uma das opções interessantes é:

```python
ipdb> request.method
'GET'
```

Outras opções interessantes são

```python
ipdb> request.GET
<QueryDict: {'name': ['John'], 'age': ['42']}>
ipdb> request.FILES
<MultiValueDict: {}>
ipdb> request.POST
<QueryDict: {}>
```

Para pegar os parâmetros vindo do request podemos fazer

```python
data = request.GET
name = data.get('name')
age = data.get('age')
# ou mais diretamente
name = request.GET.get('name')
age = request.GET.get('age')
```

Após pressionar `c` de *continue* ...

Do outro lado podemos fazer

```python
>>> result.status_code
200
>>> result.text
'pong'
>>> result.content
b'pong'
>>> result.url
'http://localhost:8000/ping/?name=John&age=42'
```

... dentre outras opções.

Por fim, se preferir você pode tirar o ipdb e fazer

```python
# views.py
def ping(request):
    print(request.GET)
    return HttpResponse('pong')
```

E usando `curl` fazer

```
curl 'localhost:8000/ping/?name=John&age=42'
```



## HttpResponseRedirect

```python
# urls.py
path('book/redirected/', v.book_redirected, name='book_redirected'),
```


```python
# views.py
from django.http import HttpResponseRedirect
from django.urls import reverse


def book_redirected(request):
    return HttpResponseRedirect(reverse('core:book_list'))
```


```html
<!-- index.html -->
<li>
  <a href="{% url 'core:book_redirected' %}">book_redirected</a>
</li>
```

## JsonResponse

```python
# urls.py
path('ping/json/', v.ping_json, name='ping_json'),
```

```python
#views.py
from django.http import JsonResponse


def ping_json(request):
    name = request.GET.get('name')
    age = request.GET.get('age')
    data = {
        'name': name,
        'age': age
    }
    return JsonResponse(data)
```

Abra um terminal e digite `python`

```python
>>> import requests
>>> url = 'http://localhost:8000/ping/json/?name=John&age=42'
>>> r = requests.get(url)
>>> r.content
b'{"name": "John", "age": "42"}'
>>> r.text
'{"name": "John", "age": "42"}'
>>> r.json()
{'name': 'John', 'age': '42'}
```

Se você não enviar parâmetros, o dicionário vai retornar valores nulos.

```python
>>> import requests
>>> url = 'http://localhost:8000/ping/json/'
>>> r = requests.get(url)
>>> r.json()
{'name': None, 'age': None}
```

Dai, o interessante seria fazer

```python
def ping_json(request):
    name = request.GET.get('name')
    age = request.GET.get('age')
    data = {}
    if name:
        data['name'] = name
    if age:
        data['age'] = age
    return JsonResponse(data)
```

Abra um terminal e digite `python`


```python
>>> import requests
>>> url = 'http://localhost:8000/ping/json/?name=John&age=42'
>>> r = requests.get(url)
>>> r.json()
{'name': 'John', 'age': '42'}
>>> 
>>> url = 'http://localhost:8000/ping/json/?name=John'
>>> r = requests.get(url)
>>> r.json()
{'name': 'John'}
>>> 
>>> url = 'http://localhost:8000/ping/json/'
>>> r = requests.get(url)
>>> r.json()
{}
```

