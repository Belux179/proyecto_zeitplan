# Generated by Django 3.2 on 2022-10-20 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_auto_20221019_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materia',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]