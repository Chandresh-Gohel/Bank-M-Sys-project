# Generated by Django 3.1.5 on 2021-01-31 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='book',
            fields=[
                ('book_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('book_name', models.CharField(max_length=15)),
                ('book_price', models.IntegerField()),
            ],
        ),
    ]
