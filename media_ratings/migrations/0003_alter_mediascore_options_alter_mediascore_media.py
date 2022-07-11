# Generated by Django 4.0.6 on 2022-07-07 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_ratings', '0002_alter_imdbscores_options_alter_media_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mediascore',
            options={'verbose_name_plural': 'TV_Series Scores'},
        ),
        migrations.AlterField(
            model_name='mediascore',
            name='media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media_ratings.tv_series'),
        ),
    ]
