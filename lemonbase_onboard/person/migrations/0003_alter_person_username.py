# Generated by Django 3.2.16 on 2023-01-02 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_auto_20221227_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='username',
            field=models.CharField(max_length=30),
        ),
    ]