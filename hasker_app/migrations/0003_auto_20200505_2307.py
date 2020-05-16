# Generated by Django 3.0.5 on 2020-05-05 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hasker_app', '0002_auto_20200505_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/'),
        ),
    ]