# Generated by Django 4.0.5 on 2022-06-20 11:25

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('scrape_status', models.IntegerField()),
                ('diary_no', models.TextField()),
                ('case_no', models.TextField()),
                ('date_of_filing', models.DateField()),
                ('applicant', models.TextField()),
                ('respondent', models.TextField()),
                ('applicant_advocate', models.TextField()),
                ('respondent_advocate', models.TextField()),
                ('view_more', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CaseStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diary_no', models.TextField()),
                ('case_type', models.TextField()),
                ('drt_detail', models.TextField()),
                ('date_of_filing', models.DateField()),
                ('case_status', models.TextField()),
                ('in_the_court_of', models.TextField()),
                ('court_no', models.TextField()),
                ('next_listing_date', models.TextField()),
                ('next_listing_purpose', models.TextField()),
                ('petitioner_name', models.TextField()),
                ('petitioner_address', models.TextField()),
                ('petitioner_additional_party', models.TextField()),
                ('petitioner_advocate_name', models.TextField()),
                ('petitioner_additional_advocate', models.TextField()),
                ('respondent_name', models.TextField()),
                ('respondent_address', models.TextField()),
                ('respondent_additional_party', models.TextField()),
                ('respondent_advocate_name', models.TextField()),
                ('respondent_additional_advocate', models.TextField()),
                ('court_details', models.TextField()),
                ('prop_details', models.TextField()),
            ],
        ),
    ]