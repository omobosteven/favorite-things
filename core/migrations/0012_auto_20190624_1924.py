# Generated by Django 2.2.2 on 2019-06-24 19:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auditlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditlog',
            name='favorite_thing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='audit_log', to='core.FavoriteThing'),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='audit_log', to=settings.AUTH_USER_MODEL),
        ),
    ]
