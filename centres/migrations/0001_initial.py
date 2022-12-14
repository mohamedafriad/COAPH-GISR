# Generated by Django 3.1 on 2021-05-09 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=300, verbose_name='الإسم')),
                ('nom_fr', models.CharField(blank=True, max_length=300, null=True, verbose_name='النسب بالفرنسية')),
            ],
            options={
                'verbose_name': 'الجهة',
                'verbose_name_plural': 'الجهات',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=300, verbose_name='الإسم')),
                ('nom_fr', models.CharField(blank=True, max_length=300, null=True, verbose_name='النسب بالفرنسية')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provinces', to='centres.region', verbose_name='الجهة')),
            ],
            options={
                'verbose_name': 'العمالة أو الإقليم',
                'verbose_name_plural': 'العمالات والأقاليم',
            },
        ),
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=300, verbose_name='الإسم')),
                ('nom_fr', models.CharField(blank=True, max_length=300, null=True, verbose_name='النسب بالفرنسية')),
                ('milieu', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'حضري'), (2, 'قروي')], default=2, null=True, verbose_name='الوسط')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communes', to='centres.province', verbose_name='العمالة أو الإقليم')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communes', to='centres.region', verbose_name='الجهة')),
            ],
            options={
                'verbose_name': 'الجماعة',
                'verbose_name_plural': 'الجماعات',
            },
        ),
        migrations.CreateModel(
            name='Centre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, verbose_name='الإسم')),
                ('telephone', models.CharField(blank=True, max_length=10, verbose_name='الهاتف')),
                ('fax', models.CharField(blank=True, max_length=10, verbose_name='الفاكس')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='البريد الالكتروني')),
                ('adresse', models.CharField(blank=True, max_length=300, verbose_name='العنوان')),
                ('gerant', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='centres', to='auth.group', verbose_name='المجموعة المسيرة')),
                ('province', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='centres', to='centres.province', verbose_name='العمالة أو الإقليم')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='centres', to='centres.region', verbose_name='الجهة')),
            ],
            options={
                'verbose_name': 'المركز',
                'verbose_name_plural': 'المراكز',
            },
        ),
    ]
