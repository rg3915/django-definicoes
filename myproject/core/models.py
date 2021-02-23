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
