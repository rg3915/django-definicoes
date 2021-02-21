# Passo a passo

Veremos passo a passo como foi construido o projeto.

> Todas as definições estão no README do projeto.

## Criar o projeto inicial

```
git clone https://gist.github.com/b363f5c4a998f42901705b23ccf4b8e8.git /tmp/boilerplatesimple
ls /tmp/boilerplatesimple
cp /tmp/boilerplatesimple/boilerplatesimple.sh .
source boilerplatesimple.sh
# Após terminar de instalar delete o arquivo boilerplatesimple.sh
rm -f boilerplatesimple.sh
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

./manage.py shell_plus

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

  <!-- Font-awesome -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">

  <!-- jQuery -->
  <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>

  <!-- Bootstrap core JS -->
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
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


