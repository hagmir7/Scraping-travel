# Generated by Django 4.1.3 on 2023-11-30 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0003_settings_favicon_settings_theme_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='footer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='settings',
            name='header',
            field=models.TextField(blank=True, null=True),
        ),
    ]