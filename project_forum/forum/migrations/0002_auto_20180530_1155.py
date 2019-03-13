# Generated by Django 2.0.5 on 2018-05-30 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Tytuł')),
                ('slug', models.SlugField(max_length=100, verbose_name='Odnośnik')),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='forum.Forum')),
            ],
            options={
                'verbose_name': 'Forum',
                'verbose_name_plural': 'Fora',
            },
        ),
        migrations.DeleteModel(
            name='MainForum',
        ),
        migrations.AlterUniqueTogether(
            name='subforum',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='subforum',
            name='content_type',
        ),
        migrations.AlterField(
            model_name='thread',
            name='forum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Forum'),
        ),
        migrations.DeleteModel(
            name='SubForum',
        ),
        migrations.AlterUniqueTogether(
            name='forum',
            unique_together={('slug', 'forum')},
        ),
    ]