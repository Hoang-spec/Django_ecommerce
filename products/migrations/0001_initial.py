# Generated by Django 5.1.5 on 2025-04-16 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
    ]
