# Generated by Django 2.1.7 on 2019-03-19 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20190319_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='assignee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
