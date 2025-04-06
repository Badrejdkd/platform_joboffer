# Generated by Django 5.2 on 2025-04-06 19:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_jobseeker_department_recruiter'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75)),
                ('description', models.TextField(max_length=191)),
                ('location', models.CharField(max_length=75)),
                ('status', models.CharField(choices=[('ongoing', 'ongoing'), ('terminated', 'terminated')], default='ongoing', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_posts', to='base.recruiter')),
            ],
            options={
                'unique_together': {('title', 'recruiter', 'status')},
            },
        ),
    ]
