# Generated by Django 3.1.2 on 2020-12-24 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0023_auto_20201224_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tests',
            name='test_name',
            field=models.CharField(max_length=1000),
        ),
    ]
