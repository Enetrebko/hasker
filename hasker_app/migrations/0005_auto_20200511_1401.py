# Generated by Django 3.0.5 on 2020-05-11 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hasker_app', '0004_remove_userprofile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='right_ind',
            field=models.BooleanField(default=False),
        ),
    ]
