# Generated by Django 3.1.2 on 2021-01-09 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0041_auto_20210106_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registers',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_registers', to='exam.tests'),
        ),
    ]