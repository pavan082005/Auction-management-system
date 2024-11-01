from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    ph_number = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Wallet(models.Model):
    wallet_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    total_incoming = models.DecimalField(max_digits=10, decimal_places=2)
    total_outgoing = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Wallet of {self.user.user.first_name} {self.user.user.last_name}"

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_title = models.CharField(max_length=100)
    item_description = models.TextField()
    item_tags = models.CharField(max_length=255)
    item_age = models.IntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_images = models.TextField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.item_title

class Auction(models.Model):
    auction_id = models.AutoField(primary_key=True)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    bid_ids = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    expiry = models.DateField()

    def __str__(self):
        return f"Auction for {self.item.item_title}"

class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bid by {self.user.user.first_name} {self.user.user.last_name} for {self.amount}"

class AuctionTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Transaction by {self.buyer.user.first_name} {self.buyer.user.last_name}"

class Lbin(models.Model):
    lbin_id = models.AutoField(primary_key=True)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    expiry_time = models.TimeField()
    bid = models.BooleanField()

    def __str__(self):
        return f"LBIN for {self.item.item_title}"

class LbinTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    lbin = models.ForeignKey(Lbin, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"LBIN Transaction by {self.buyer.user.first_name} {self.buyer.user.last_name}"

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=100)
    landmark = models.CharField(max_length=255)
    coordinate = models.CharField(max_length=50)

    def __str__(self):
        return self.location_name

class Discussion(models.Model):
    discussion_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    message = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Discussion by {self.author.user.first_name} {self.author.user.last_name}"

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    victim = models.ForeignKey(Profile, related_name='victim', on_delete=models.CASCADE)
    accused = models.ForeignKey(Profile, related_name='accused', on_delete=models.CASCADE)
    report_message = models.TextField()

    def __str__(self):
        return f"Report by {self.victim.user.first_name} {self.victim.user.last_name}"
