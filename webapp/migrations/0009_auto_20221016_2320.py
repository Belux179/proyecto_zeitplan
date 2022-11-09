# Generated by Django 3.2 on 2022-10-16 23:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20221016_2253'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aula',
            old_name='state_model',
            new_name='state',
        ),
        migrations.RenameField(
            model_name='horario',
            old_name='duracion_hora',
            new_name='duracion_periodo_minute',
        ),
        migrations.RemoveField(
            model_name='horario',
            name='duracion_minuto',
        ),
        migrations.RemoveField(
            model_name='horario',
            name='no_periodos',
        ),
        migrations.AddField(
            model_name='horario',
            name='cantidad_periodo',
            field=models.IntegerField(default=7),
        ),
        migrations.AddField(
            model_name='horario',
            name='ciclo',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='horario',
            name='duracion_periodo_hour',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='horario',
            name='no_page',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='profesor',
            name='profesion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='hora_inicio',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='horario',
            name='status_model',
            field=models.BooleanField(default=False),
        ),
    ]
