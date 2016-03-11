# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('tiempo_subida', models.DateTimeField(blank=True)),
                ('user_id', models.IntegerField()),
                ('x_subida', models.CharField(max_length=100)),
                ('y_subida', models.CharField(max_length=100)),
                ('tipo_transporte', models.CharField(max_length=100)),
                ('serviciosentidovariante', models.CharField(max_length=100)),
                ('tipo_dia', models.CharField(max_length=100)),
                ('nviaje', models.IntegerField()),
                ('netapa', models.IntegerField()),
                ('x_bajada', models.CharField(max_length=100)),
                ('y_bajada', models.CharField(max_length=100)),
                ('tiempo_bajada', models.CharField(max_length=100)),
                ('par_subida', models.CharField(max_length=100)),
                ('par_bajada', models.CharField(max_length=100)),
                ('zona_subida', models.CharField(max_length=100)),
                ('zona_bajada', models.CharField(max_length=100)),
                ('adulto', models.CharField(max_length=100)),
            ],
        ),
    ]
