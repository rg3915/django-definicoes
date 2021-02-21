# Generated by Django 2.2.19 on 2021-02-21 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='título')),
            ],
            options={
                'verbose_name': 'livro',
                'verbose_name_plural': 'livros',
                'ordering': ('title',),
            },
        ),
    ]