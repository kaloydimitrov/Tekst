# Generated by Django 4.2.13 on 2024-08-27 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='extra_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]