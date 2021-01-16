# Generated by Django 3.1.3 on 2021-01-16 10:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210115_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='auction_end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 23, 10, 25, 29, 270432)),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='listing_id',
            field=models.ManyToManyField(null=True, related_name='listings', to='auctions.Listing'),
        ),
    ]
