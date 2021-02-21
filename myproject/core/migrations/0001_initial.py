# Generated by Django 2.2.19 on 2021-02-21 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'pessoa',
                'verbose_name_plural': 'pessoas',
                'ordering': ('name',),
            },
        ),
    ]