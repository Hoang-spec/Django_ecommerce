# Generated by Django 5.1.5 on 2025-04-16 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='type',
            field=models.CharField(default='general', max_length=50),
        ),
    ]
