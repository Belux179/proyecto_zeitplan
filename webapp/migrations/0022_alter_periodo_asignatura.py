# Generated by Django 3.2 on 2022-10-25 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0021_periodo_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodo',
            name='asignatura',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.asignatura'),
        ),
    ]
