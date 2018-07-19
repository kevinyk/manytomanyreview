# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-19 20:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg_app', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchasing_buyer', to='login_reg_app.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='users_who_purchased',
        ),
        migrations.AddField(
            model_name='purchase',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased_product', to='login_reg_app.Product'),
        ),
    ]
