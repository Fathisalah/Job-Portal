# Generated by Django 5.0.2 on 2024-12-26 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_alter_job_options_job_benefits_job_location_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobapplication',
            options={'ordering': ['-applied_at']},
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='cover_letter',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('reviewing', 'Reviewing'), ('shortlisted', 'Shortlisted'), ('rejected', 'Rejected'), ('selected', 'Selected')], default='pending', max_length=20),
        ),
    ]
