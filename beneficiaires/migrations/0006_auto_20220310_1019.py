# Generated by Django 3.1 on 2022-03-10 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiaires', '0005_auto_20210608_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiaire',
            name='sexe',
            field=models.PositiveSmallIntegerField(choices=[(1, 'ذكر'), (2, 'أنثى')], verbose_name='النوع'),
        ),
    ]
