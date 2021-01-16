from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta


class User(AbstractUser):
    pass


class Listing(models.Model):
    EQUIPMENT = 'Equipment'
    WEAPONS = 'Weapons'
    VEHICLES = 'Vehicles'
    ARTIFACTS = 'Artifacts'
    MISC = 'Misc'
    CATEGORY_CHOICES = [
        (EQUIPMENT, 'Equipment'),
        (WEAPONS, 'Weapons'),
        (VEHICLES, 'Vehicles'),
        (ARTIFACTS, 'Artifacts'),
        (MISC, 'Misc'),
    ]

    id = models.AutoField(auto_created=True, primary_key=True,
                          serialize=False, verbose_name='ID')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owners")
    title = models.CharField(max_length=64)
    auction_end_date = models.DateTimeField(
        default=datetime.now()+timedelta(days=7))
    listing_image = models.ImageField(upload_to='images', blank=True)
    description = models.CharField(max_length=128)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=16, choices=CATEGORY_CHOICES, default=EQUIPMENT)

    def __str__(self):
        return f"{self.title}"

    def get_categories(self):
        return self.CATEGORY_CHOICES


class Winner(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="winners")
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="auction_listings")


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchlist_items")
    listing_id = models.ManyToManyField(
        Listing, blank=True, related_name="listings")

    def __str__(self):
        return f"{self.user}'s Watchlist"


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_bids")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_time = models.DateTimeField()
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"${self.bid_amount} - submitted by {self.user} on {self.bid_time}"


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments")
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing_comments")
    comment_time = models.DateTimeField()
    content = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.content}"
