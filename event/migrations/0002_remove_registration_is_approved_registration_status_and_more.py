# Generated by Django 4.2.20 on 2025-04-09 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='is_approved',
        ),
        migrations.AddField(
            model_name='registration',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='active', max_length=20),
        ),
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('sold_out', 'Sold Out'), ('on_hold', 'On Hold'), ('cancelled', 'Cancelled')], default='available', max_length=20),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('inactive', 'Inactive'), ('cancelled', 'Cancelled'), ('archived', 'Archived')], default='draft', max_length=20),
        ),
    ]
