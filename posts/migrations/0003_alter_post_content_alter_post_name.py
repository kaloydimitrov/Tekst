# Generated by Django 4.2.13 on 2024-05-19 20:44

from django.db import migrations, models
import posts.validators


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(validators=[posts.validators.validate_len]),
        ),
        migrations.AlterField(
            model_name='post',
            name='name',
            field=models.CharField(max_length=100, validators=[posts.validators.validate_len]),
        ),
    ]
