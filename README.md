# django-definicoes

Django: Guia de definições para redirect, reverse, reverse_lazy, HttpResponse entres outros


## Este projeto foi feito com:

* [Python 3.8.2](https://www.python.org/)
* [Django 2.2.16](https://www.djangoproject.com/)

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/rg3915/django-definicoes.git
cd django-definicoes
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
```

Leia o [passo a passo](passo-a-passo.md).


# Definições

Definição e explicação com exemplos de:

### [django.shortcuts](https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/)

* [x] [render_to_string](#render_to_string) django.template.loader
* [x] [render_to_response](#render_to_response) django.shortcuts
* [x] [HttpResponse](#HttpResponse) django.http
* [x] [render](#render) django.shortcuts
* [x] [redirect](#redirect) django.shortcuts

### [django.urls](https://docs.djangoproject.com/en/3.0/ref/urlresolvers/)

* [x] [reverse](#reverse) django.urls
* [x] [reverse_lazy](#reverse_lazy) django.urls
* [x] [resolve](#resolve) django.urls
* [x] [resolve_url](#resolve_url) django.shortcuts

### [django.http](https://docs.djangoproject.com/en/3.0/ref/request-response/)

* [x] [HttpRequest](#HttpRequest) django.http
* [x] [HttpResponseRedirect](#HttpResponseRedirect) django.http
* [x] [JsonResponse](#JsonResponse) django.http


# render_to_string

https://docs.djangoproject.com/en/3.1/topics/templates/#django.template.loader.render_to_string

[source code](https://docs.djangoproject.com/en/2.2/_modules/django/template/loader/#render_to_string)

**Definição do código fonte**:

> Carrega um template e renderiza com um contexto. Retorna uma string.

**Definição da doc**:

`render_to_string(template_name, context=None, request=None, using=None)`

* **render_to_string()** carrega um template e chama o método `render()` imediatamente.

* **template_name**

O nome do template a ser carregado e renderizado.

* **context**

Um dicionário pode ser usado no contexto do template para ser renderizado.

* **request**

An optional HttpRequest that will be available during the template’s rendering process.

* **using**

An optional template engine NAME. The search for the template will be restricted to that engine.



Digite `./manage.py shell` e faça:

```python
from django.template.loader import render_to_string

rendered = render_to_string('my_template.html', {'name': 'render_to_string'})
rendered
```

Então, em `views.py`, podemos fazer:

```python
from django.http import HttpResponse

def my_http_response(request):
    return HttpResponse(rendered)
```

**Exemplo:** Aliás, um bom exemplo de uso é a preparação de mensagem para envio de e-mail.



# render_to_response

https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/#django.shortcuts.render_to_response

[source code](https://docs.djangoproject.com/en/2.2/_modules/django/shortcuts/#render_to_response)

Obsoleto desde a versão 2.0.

**Definição do código fonte**:

> Retorna um [HttpResponse](https://docs.djangoproject.com/en/3.0/ref/request-response/#httpresponse-objects) cujo contexto é preenchido com o resultado da chamada.

**Definição da doc**:

`render_to_response(template_name, context=None, content_type=None, status=None, using=None)`


```python
from django.shortcuts import render_to_response


def my_render_to_response(request):
    return render_to_response('my_template.html', {'name': 'render_to_response'})
```

Era usado antes do [render](https://docs.djangoproject.com/en/3.0/topics/http/shortcuts/#render).


# HttpResponse

https://docs.djangoproject.com/en/3.0/ref/request-response/#httpresponse-objects

[source code](https://docs.djangoproject.com/en/2.2/_modules/django/http/response/#HttpResponse)

**Definição do código fonte**:

É a resposta da requisição HTTP.

**Definição da doc**:

`class HttpResponse`

Em contraste com os objetos `HttpRequest`, que são criados automaticamente pelo Django, os objetos `HttpResponse` são de sua responsabilidade. Cada visualização que você escreve é ​​responsável por instanciar, preencher e retornar um `HttpResponse`.


**Exemplo:**

```python
# views.py
from django.http import HttpResponse


def users(request):
    return HttpResponse('<h1>Users</h1>')

def user_detail(request, pk):
    return HttpResponse(f'User {pk}')
```

```python
# urls.py
path('user/', v.users, name='users'),
path('user/<int:pk>/', v.user_detail, name='user_detail'),
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

```python
>>> import requests
>>> url = 'http://localhost:8000/ping/?name=John&age=42'
>>> r = requests.get(url)
>>> r.content
b'pong John'
```

Veja a saída do print:

`<QueryDict: {'name': ['John'], 'age': ['42']}>`



# render

https://docs.djangoproject.com/en/3.0/topics/http/shortcuts/#render

[source code](https://docs.djangoproject.com/en/2.2/_modules/django/shortcuts/#render)

**Definição do código fonte**:

É uma função que retorna um `HttpResponse`, e renderiza um template HTML com o contexto preenchido com o resultado do `render_to_string` passado como argumento.

**Definição da doc**:

`render(request, template_name, context=None, content_type=None, status=None, using=None)`

Combina um template com um dicionário de contexto e retorna um `HttpResponse`.

Argumentos requeridos: `request` e `template_name`.

Argumentos opcionais: `context`, `content_type`, `status`, `using`.

**Exemplo:**

```python
# views.py
from django.shortcuts import render


def index(request):
    template_name = 'index.html'
    return render(request, template_name)
```

```python
# urls.py
from django.urls import path
from myproject.core import views as v


app_name = 'core'


urlpatterns = [
    path('', v.index, name='index'),
]
```

# redirect

https://docs.djangoproject.com/en/3.0/topics/http/shortcuts/#redirect

[source code](https://docs.djangoproject.com/en/2.2/_modules/django/shortcuts/#redirect)

Retorna um [HttpResponseRedirect](https://docs.djangoproject.com/en/3.0/ref/request-response/#django.http.HttpResponseRedirect) para a url apropriada com os argumentos passados.

Os argumentos podem ser:

* Um modelo: a função `get_absolute_url()` deve ser chamada.
* Um nome de view, possivelmente com argumentos: `reverse()` deve ser usado pra resolver o nome reverso (nome da url).
* Uma url absoluta ou relativa, quando for redirecionado pra outro local.


### Um modelo

A função `get_absolute_url()` deve ser chamada.


```python
# models.py
from django.db import models
from django.urls import reverse_lazy


class Person(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'pessoa'
        verbose_name_plural = 'pessoas'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('core:person_redirected', kwargs={'pk': self.pk})
```

```python
# urls.py
path('person/<int:pk>/', v.person_detail, name='person_detail'),
path('person/redirected/<int:pk>/', v.person_redirected, name='person_redirected'),
```

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

Possivelmente com argumentos: `reverse()` deve ser usado pra resolver o nome reverso (nome da url).

```python
# urls.py
path('person/', v.persons, name='persons'),
path('person/redirected/', v.persons_redirected, name='persons_redirected'),
```

```python
# views.py
def persons_redirected(request):
    return HttpResponse(f'<p>Você foi redirecionado!</p>')


def persons(request):
    print('Você será redirecionado')
    return redirect('core:persons_redirected')
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


# reverse

https://docs.djangoproject.com/en/2.2/ref/urlresolvers/#reverse

[source code](https://docs.djangoproject.com/en/2.2/_modules/django/urls/base/#reverse)

**Definição**

`reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)`

O `reverse` permite que você passe o nome da url como argumento.


**Exemplo:**

```python
# views.py
from django.http import HttpResponse


def users(request):
    return HttpResponse('<h1>Users</h1>')


def user_detail(request, pk):
    return HttpResponse(f'User {pk}')
```


```python
# urls.py
from django.urls import path
from myproject.core import views as v


app_name = 'core'


urlpatterns = [
    path('user/', v.users, name='users'),
    path('user/<int:pk>/', v.user_detail, name='user_detail'),
]
```



```python
# shell_plus
from django.urls import reverse
>>> reverse('core:users')
'/user/'

reverse('core:user_detail', kwargs={'pk': 1})
'/user/1/'
```



# reverse_lazy

https://docs.djangoproject.com/en/2.2/ref/urlresolvers/#reverse-lazy

É uma versão *lazily evaluated* do `reverse()`.

Ou seja, ela é uma função "preguiçosa".

* fornece uma url para um atributo baseado em Class Based View.
* fornece uma url para um decorator, `login_url` por exemplo.


```python
from django.urls import reverse_lazy


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

Usando com o `login_url`

```python
from django.contrib.auth.decorators import login_required


@login_required(login_url=reverse_lazy('admin:login'))
def users(request):
    return HttpResponse('<h1>Users</h1>')
```

https://simpleisbetterthancomplex.com/article/2016/09/12/shortcuts.html


# resolve

https://docs.djangoproject.com/en/2.2/ref/urlresolvers/#resolve

[source code](https://docs.djangoproject.com/en/2.2/_modules/django/urls/base/#resolve)

É usado pra encontrar o nome da url. No parâmetro é passada a url relativa.

```python
from django.urls import resolve
>>> match = resolve('/person/')
>>> match.url_name
'persons'
>>> match = resolve('/person/1/')
>>> match.url_name
'person_detail'
```



# resolve_url

https://docs.djangoproject.com/pt-br/2.2/_modules/django/shortcuts/

```python
from django.shortcuts import resolve_url
>>> resolve_url('core:persons')
'/person/'
>>> resolve_url('core:person_detail', pk=1)
'/person/1/'
```


# HttpRequest

https://docs.djangoproject.com/en/3.0/ref/request-response/#httprequest-objects

[source code](https://docs.djangoproject.com/en/2.2/_modules/django/http/request/#HttpRequest)

Exemplo 29 de Project: jaisting - Author: himrock922

https://www.programcreek.com/python/example/50074/django.http.HttpRequest

```python
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')
```

`HttpRequest` é a classe Python que faz a requisição.

`HttpResponse` é a resposta da requisição.

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



# HttpResponseRedirect

https://docs.djangoproject.com/en/3.0/ref/request-response/#django.http.HttpResponseRedirect

[source code](https://docs.djangoproject.com/en/2.2/_modules/django/http/response/#HttpResponseRedirect)

Exemplos em

https://simpleisbetterthancomplex.com/article/2016/09/12/shortcuts.html

```python
from django.http import HttpResponseRedirect

def book_redirected(request):
    return HttpResponseRedirect(reverse('core:book_list'))
```



# JsonResponse

https://docs.djangoproject.com/en/3.0/ref/request-response/#jsonresponse-objects

[source code](https://docs.djangoproject.com/en/2.2/_modules/django/http/response/#JsonResponse)



**Exemplo:**

```python
# urls.py
from django.urls import path
from myproject.core import views as v


urlpatterns = [
    path('ping/json/', v.ping_json, name='ping_json'),
]
```


```python
# views.py
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

Mais alguns links:

https://www.mattlayman.com/django-riffs/views-on-django/


https://simpleisbetterthancomplex.com/article/2016/09/12/shortcuts.html

