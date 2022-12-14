# Generated by Django 3.1 on 2021-06-15 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('beneficiaires', '0005_auto_20210608_1251'),
        ('centres', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EtapeProjet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, verbose_name='المرحلة')),
                ('ordre', models.PositiveSmallIntegerField(null=True, verbose_name='الترتيب')),
            ],
            options={
                'verbose_name': 'مرحلة الطلب',
                'verbose_name_plural': 'مراحل الطلب',
            },
        ),
        migrations.CreateModel(
            name='ExecuteurProjet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nature_tuteur', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'المستفيد'), (2, 'ولي الامر (الأب)'), (3, 'ولي الأمر (الأم)'), (4, 'آخر')], default=1, null=True, verbose_name='طبيعة حامل المشروع')),
                ('nom_tuteur_ar', models.CharField(blank=True, max_length=30, verbose_name='اسم ولي الأمر')),
                ('cin_tuteur', models.CharField(blank=True, max_length=15, verbose_name='رقم بطاقة ولي الأمر')),
                ('beneficiaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='porteur', to='beneficiaires.beneficiaire', verbose_name='المستفيد')),
            ],
            options={
                'verbose_name': 'Porteur Projet',
                'verbose_name_plural': 'Porteurs Projet',
            },
        ),
        migrations.CreateModel(
            name='Projet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(max_length=200, verbose_name='اسم المشروع')),
                ('date_demande', models.DateField(blank=True, null=True, verbose_name='تاريخ الطلب')),
                ('description', models.CharField(blank=True, max_length=500, verbose_name='التوصيف')),
                ('montant_total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='المبلغ الاجمالي')),
                ('montant_demande', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='المبلغ المطلوب')),
                ('montant_contribution', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='المساهمة الشخصية')),
                ('secteur', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'الخدمات'), (2, 'التجارة'), (3, 'الصناعة'), (4, 'النقل'), (5, 'الصناعة التقليدية'), (6, 'آخر')], null=True, verbose_name='القطاع')),
                ('forme_juridique', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'المقاول الذاتي'), (2, 'شركة'), (3, 'تعاونية'), (4, 'آخر')], null=True, verbose_name='الصيغة القانونية')),
                ('lieu_adresse', models.CharField(default='كلميم', max_length=20, verbose_name='مكان التنفيذ')),
                ('piece_cin', models.BooleanField(blank=True, null=True, verbose_name='نسخة من البطاقة الوطنية')),
                ('piece_ramed', models.BooleanField(blank=True, null=True, verbose_name='نسخة من الراميد')),
                ('piece_certificat', models.BooleanField(blank=True, null=True, verbose_name='الشهادة الطبية')),
                ('piece_engagement', models.BooleanField(blank=True, null=True, verbose_name='التزام بتوفير المحل')),
                ('piece_devis', models.BooleanField(blank=True, null=True, verbose_name='عرض الأثمان التقديري')),
                ('piece_local', models.BooleanField(blank=True, null=True, verbose_name='مقر انجاز المشروع')),
                ('piece_conv_accom', models.BooleanField(blank=True, null=True, verbose_name='اتفاقية المواكبة')),
                ('piece_conv_finan', models.BooleanField(blank=True, null=True, verbose_name='اتفاقية التمويل')),
                ('num_cheque', models.CharField(blank=True, max_length=20, null=True, verbose_name='رقم الشيك')),
                ('date_cheque', models.DateField(blank=True, null=True, verbose_name='تاريخ الشيك')),
                ('date_lancement', models.DateField(blank=True, null=True, verbose_name='تاريخ الانطلاقة')),
                ('beneficiaire', models.ManyToManyField(through='projets.ExecuteurProjet', to='beneficiaires.Beneficiaire', verbose_name='المستفيد')),
                ('centre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projets', to='centres.centre', verbose_name='المركز')),
            ],
            options={
                'verbose_name': 'المشروع',
                'verbose_name_plural': 'المشاريع',
            },
        ),
        migrations.CreateModel(
            name='Visite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_visite', models.DateField(verbose_name='تاريخ الزيارة')),
                ('observation', models.CharField(blank=True, max_length=700, null=True, verbose_name='ملاحظات')),
                ('projet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visites', to='projets.projet', verbose_name='المشروع')),
            ],
            options={
                'verbose_name': 'الزيارة',
                'verbose_name_plural': 'الزيارات',
            },
        ),
        migrations.CreateModel(
            name='SuiviProjet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_etap', models.DateField(blank=True, null=True, verbose_name='تاريخ المرحلة')),
                ('commentaire', models.CharField(blank=True, max_length=300, verbose_name='ملاحظات')),
                ('etape', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suivi', to='projets.etapeprojet', verbose_name='المرحلة')),
                ('projet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suivi', to='projets.projet', verbose_name='المشروع')),
            ],
            options={
                'verbose_name': 'مرحلة المشروع',
                'verbose_name_plural': 'مراحل المشروع',
            },
        ),
        migrations.AddField(
            model_name='projet',
            name='etape',
            field=models.ManyToManyField(blank=True, related_name='projets', through='projets.SuiviProjet', to='projets.EtapeProjet', verbose_name='المرحلة'),
        ),
        migrations.AddField(
            model_name='projet',
            name='lieu_commune',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projets', to='centres.commune', verbose_name='الجماعة'),
        ),
        migrations.AddField(
            model_name='projet',
            name='lieu_province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projets', to='centres.province', verbose_name='العمالة أو الإقليم'),
        ),
        migrations.AddField(
            model_name='projet',
            name='lieu_region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projets', to='centres.region', verbose_name='الجهة'),
        ),
        migrations.AddField(
            model_name='executeurprojet',
            name='projet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='porteur', to='projets.projet', verbose_name='المشروع'),
        ),
        migrations.CreateModel(
            name='Avis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commission', models.PositiveSmallIntegerField(choices=[(1, 'الاقليمية'), (2, 'الجهوية'), (3, 'المركزية')], verbose_name='اللجنة')),
                ('date_avis', models.DateField(verbose_name='تاريخ ابداء الرأي')),
                ('num_pv', models.CharField(blank=True, max_length=10, null=True, verbose_name='رقم المحضر')),
                ('decision', models.PositiveSmallIntegerField(choices=[(1, 'مقبول'), (2, 'غير مقبول'), (3, 'اعادة الصياغة')], verbose_name='القرار')),
                ('note', models.PositiveSmallIntegerField(default=0, verbose_name='التنقيط')),
                ('observation', models.CharField(blank=True, max_length=700, null=True, verbose_name='ملاحظات')),
                ('montant_approuve', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='المبلغ المصادق عليه')),
                ('nbre_tranche', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='عدد الأشطر')),
                ('projet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avis', to='projets.projet', verbose_name='المشروع')),
            ],
            options={
                'verbose_name': 'الرأي',
                'verbose_name_plural': 'الرأي',
            },
        ),
    ]
