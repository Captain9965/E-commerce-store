# Generated by Django 3.2.8 on 2022-09-08 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20220903_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='result_description',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
