# Generated by Django 3.2 on 2022-08-22 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20220821_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='grado',
            name='state',
            field=models.BooleanField(default=True),
        ),
    ]
