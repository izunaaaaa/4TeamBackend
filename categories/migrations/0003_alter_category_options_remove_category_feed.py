# Generated by Django 4.2 on 2023-04-06 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='feed',
        ),
    ]
