# Generated by Django 2.2.3 on 2019-07-05 19:33

import core.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20190705_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=core.models.CICharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='favoritething',
            name='title',
            field=core.models.CICharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=core.models.CIEmailField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='firstname',
            field=core.models.CICharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastname',
            field=core.models.CICharField(max_length=255),
        ),
    ]