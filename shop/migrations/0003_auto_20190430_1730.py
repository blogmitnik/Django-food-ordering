# Generated by Django 2.2 on 2019-04-30 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_category_select'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='select',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Available'), (1, 'Not available')], default=1),
        ),
    ]