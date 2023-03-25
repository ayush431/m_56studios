# Generated by Django 3.2.9 on 2022-04-12 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_question_images_x'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='flagged_reason',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('For Review', 'For Review'), ('Approved', 'Approved'), ('Rejected', 'Rejected By Editor'), ('Image Rejected', 'Image Rejected'), ('Question Rejected', 'Question Rejected'), ('Ready To Publish', 'Ready To Publish'), ('Published', 'Published'), ('ReReview', 'Re Review'), ('Discarded', 'Discarded'), ('Overwritten', 'Overwritten'), ('Flagged', 'Flagged')], default='Draft', max_length=50, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='status_log',
            name='new_status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('For Review', 'For Review'), ('Approved', 'Approved'), ('Rejected', 'Rejected By Editor'), ('Image Rejected', 'Image Rejected'), ('Question Rejected', 'Question Rejected'), ('Ready To Publish', 'Ready To Publish'), ('Published', 'Published'), ('ReReview', 'Re Review'), ('Discarded', 'Discarded'), ('Overwritten', 'Overwritten'), ('Flagged', 'Flagged')], max_length=50, null=True, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='status_log',
            name='old_status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('For Review', 'For Review'), ('Approved', 'Approved'), ('Rejected', 'Rejected By Editor'), ('Image Rejected', 'Image Rejected'), ('Question Rejected', 'Question Rejected'), ('Ready To Publish', 'Ready To Publish'), ('Published', 'Published'), ('ReReview', 'Re Review'), ('Discarded', 'Discarded'), ('Overwritten', 'Overwritten'), ('Flagged', 'Flagged')], max_length=50, null=True, verbose_name='Type'),
        ),
    ]