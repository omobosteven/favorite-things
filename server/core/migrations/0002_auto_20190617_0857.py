# Generated by Django 2.2.2 on 2019-06-17 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='categoryuser',
            unique_together={('category', 'user')},
        ),
    ]
