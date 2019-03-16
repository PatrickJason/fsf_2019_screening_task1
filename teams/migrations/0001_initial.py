# Generated by Django 2.1.7 on 2019-03-15 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('members', models.ManyToManyField(through='teams.TeamMember', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='teammember',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='teams.Teams'),
        ),
        migrations.AddField(
            model_name='teammember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_teams', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='teammember',
            unique_together={('team', 'user')},
        ),
    ]
