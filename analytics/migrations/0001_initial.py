# Generated by Django 4.2.20 on 2025-04-01 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_registrations', models.PositiveIntegerField(default=0)),
                ('total_views', models.PositiveIntegerField(default=0)),
                ('total_check_ins', models.PositiveIntegerField(default=0)),
                ('engagement_score', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
