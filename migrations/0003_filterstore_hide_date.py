# Generated by Django 5.0.3 on 2024-04-22 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_filters_stoex', '0002_alter_filterstore_options_filterstore_all_users_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='filterstore',
            name='hide_date',
            field=models.BooleanField(default=False, help_text='If the date should be hidden in the display.  Only applies if name is not blank', verbose_name='hide date'),
        ),
    ]
