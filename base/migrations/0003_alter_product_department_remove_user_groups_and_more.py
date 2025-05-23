# Generated by Django 5.2.1 on 2025-05-22 06:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('base', '0002_alter_product_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='department',
            field=models.ManyToManyField(to='base.department'),
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
    ]
