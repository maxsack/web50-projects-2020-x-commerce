# Generated by Django 4.1.2 on 2022-10-30 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_bid_alter_listing_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.IntegerField(),
        ),
    ]
