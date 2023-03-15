from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Client3DS(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    consoleid = models.CharField(max_length=12, null=False)
    devicetoken = models.CharField(max_length=21, null=False)
    is_terminated = models.BooleanField(default=False)
    balance = models.IntegerField(default=0)
    language = models.CharField(max_length=3, null=False)
    region = models.CharField(max_length=3, null=False)
    country = models.CharField(max_length=3, null=False)
    uniquekey = models.CharField(max_length=10, null=False)
    def __str__(self):
        return "3DS "+self.consoleid

class User(AbstractUser):
    linked_ds = models.ForeignKey(Client3DS, null=True, on_delete=models.CASCADE)

class customTitleID(models.Model):
    tid = models.CharField(max_length=18, null=False)
    related_to = models.ForeignKey(Client3DS, null=False, on_delete=models.CASCADE)
    def __str__(self):
        return "Title "+self.tid+" for user "+self.related_to.consoleid

class publisher(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    publisher_name = models.CharField(max_length=20)
    def __str__(self):
        return self.publisher_name

class category(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    index = models.IntegerField(default=0, null=False)
    name = models.CharField(max_length=25)
    standard = models.BooleanField(default=False)
    icon_url = models.TextField(null=False)
    banner_url = models.TextField(null=False)
    new = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    def __str__(self):
        return "Category "+self.name

class genre(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class platform(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Title(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    tid = models.CharField(max_length=16, null=False)
    name = models.CharField(max_length=25)
    desc = models.TextField(default="", null=False)
    thumbnail_url = models.TextField(null=False)
    icon_url = models.TextField(null=False)
    banner_url = models.TextField(null=False)
    publisher = models.ForeignKey(publisher, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, null=False)
    product_code = models.CharField(max_length=30)
    new = models.BooleanField(default=True)
    public = models.BooleanField(default=True)
    category = models.ForeignKey(category, on_delete=models.DO_NOTHING, null=True, blank=True)
    genre = models.ForeignKey(genre, null=False, on_delete=models.CASCADE)
    in_app_purchase = models.BooleanField(default=False)
    platform = models.ForeignKey(platform, null=False, on_delete=models.CASCADE)
    price = models.IntegerField(default=0, null=False)
    version = models.IntegerField(default=1024)
    is_not_downloadable = models.BooleanField(default=False)
    ticket_id = models.CharField(max_length=16, null=False)
    ticket = models.TextField(null=False)
    size = models.IntegerField(default=0)
    ticket_available = models.BooleanField(default=True)
    def __str__(self):
        return self.name+" by "+self.publisher.publisher_name+" published on "+str(self.date)

class movie(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    name = models.CharField(max_length=25)
    thumbnail_url = models.TextField(null=False)
    banner_url = models.TextField(null=False)
    is_3d = models.BooleanField(default=False)
    moflex_url = models.TextField(null=False)
    time_in_sec = models.IntegerField(null=False)
    date = models.DateField(auto_now_add=True, null=False)
    category = models.ForeignKey(category, on_delete=models.DO_NOTHING, null=True, blank=True)
    new = models.BooleanField(default=True, null=False)
    def __str__(self):
        return self.name

class ownedTitle(models.Model):
    title = models.ForeignKey(Title, null=False, on_delete=models.CASCADE)
    version = models.IntegerField(null=False)
    owner = models.ForeignKey(Client3DS, null=False, on_delete=models.CASCADE)
    def __str__(self):
        return "Title "+self.title.name+" owned by "+self.owner.consoleid

class wishlistedTitle(models.Model):
    title = models.ForeignKey(Title, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(Client3DS, null=False, on_delete=models.CASCADE)
    def __str__(self):
        return "Wishlisted title "+self.title.name+" wanted by "+self.owner.consoleid

class announcement(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    title = models.CharField(max_length=50, null=False)
    content = models.TextField(null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)
    is_banner = models.BooleanField(default=False)
    banner_url = models.TextField(null=True, blank=True)
    def __str__(self):
        return "Announcement "+self.title

class motd(models.Model):
    content = models.TextField(null=False)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.content
    
class redeemableCard(models.Model):
    code = models.CharField(max_length=16, null=False)
    used = models.BooleanField(default=False)
    is_money = models.BooleanField(default=True)
    content = models.CharField(max_length=16, null=False)
    def __str__(self):
        return self.code
    
class searchCategory(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    name = models.CharField(max_length=35)
    platform_list = models.TextField()
    def __str__(self):
        return self.name
