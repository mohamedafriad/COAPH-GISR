# Generated by Django 3.2.3 on 2022-07-29 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiaires', '0006_auto_20220310_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiaire',
            name='situation_prof',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'RECHERCHE UN EMPLOI'), (2, 'EN ACTIVITE'), (3, 'EN FORMATION'), (4, 'AUTRE')], default=1, verbose_name='Situation Socio Professionnelle'),
        ),
    ]