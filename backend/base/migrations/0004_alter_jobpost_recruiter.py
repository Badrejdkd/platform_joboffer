# Generated by Django 5.2 on 2025-05-04 21:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_recruiter_profession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='recruiter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recruiter', to='base.recruiter'),
        ),
    ]
