# Generated by Django 3.1 on 2021-12-16 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projets', '0002_auto_20210615_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projet',
            name='piece_certificat',
            field=models.BooleanField(choices=[(True, 'نعم'), (False, 'لا')], default=False, verbose_name='الشهادة الطبية'),
        ),
        migrations.AlterField(
            model_name='projet',
            name='piece_cin',
            field=models.BooleanField(choices=[(True, 'نعم'), (False, 'لا')], default=False, verbose_name='نسخة من البطاقة الوطنية'),
        ),
        migrations.AlterField(
            model_name='projet',
            name='piece_conv_accom',
            field=models.BooleanField(choices=[(True, 'نعم'), (False, 'لا')], default=False, verbose_name='اتفاقية المواكبة'),
        ),
        migrations.AlterField(
            model_name='projet',
            name='piece_conv_finan',
            field=models.BooleanField(choices=[(True, 'نعم'), (False, 'لا')], default=False, verbose_name='اتفاقية التمويل'),
        ),
        migrations.AlterField(
            model_name='projet',
            name='piece_devis',
            field=models.BooleanField(choices=[(True, 'نعم'), (False, 'لا')], default=False, verbose_name='عرض الأثمان التقديري'),
        ),
        migrations.AlterField(
            model_name='projet',
            name='piece_engagement',
            field=models.BooleanField(choices=[(True, 'نعم'), (False, 'لا')], default=False, verbose_name='التزام بتوفير المحل'),
        ),
        migrations.AlterField(
            model_name='projet',
            name='piece_local',
            field=models.BooleanField(choices=[(True, 'نعم'), (False, 'لا')], default=False, verbose_name='مقر انجاز المشروع'),
        ),
        migrations.AlterField(
            model_name='projet',
            name='piece_ramed',
            field=models.BooleanField(choices=[(True, 'نعم'), (False, 'لا')], default=False, verbose_name='نسخة من الراميد'),
        ),
    ]
