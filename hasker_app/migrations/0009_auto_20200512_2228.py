# Generated by Django 3.0.5 on 2020-05-12 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hasker_app', '0008_auto_20200512_1904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='right_ind',
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hasker_app.Question'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(null=True, upload_to='pictures/'),
        ),
        migrations.CreateModel(
            name='UserVotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.ManyToManyField(blank=True, related_name='users_voted', to='hasker_app.Answer')),
                ('questions', models.ManyToManyField(blank=True, related_name='users_voted', to='hasker_app.Question')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]