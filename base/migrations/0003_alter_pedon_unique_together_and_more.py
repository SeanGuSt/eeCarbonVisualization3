# Generated by Django 5.1.3 on 2025-02-07 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_synonym_name_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pedon',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='site',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='pedon',
            name='pedon_id',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='site',
            name='site_id',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='pedon',
            unique_together={('name', 'pedon_id', 'site')},
        ),
        migrations.AlterUniqueTogether(
            name='site',
            unique_together={('name', 'site_id', 'source')},
        ),
    ]
