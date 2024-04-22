from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Client3DS(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    consoleid = models.CharField(max_length=12, null=False)
    devicecert_consoleid = models.CharField(max_length=8, null=True, blank=True)
    devicetoken = models.CharField(max_length=21, null=False)
    is_terminated = models.BooleanField(default=False)
    balance = models.IntegerField(default=0)
    language = models.CharField(max_length=3, null=False)
    region = models.CharField(max_length=3, null=False)
    country = models.CharField(max_length=3, null=False)
    uniquekey = models.CharField(max_length=21, null=False)
    def __str__(self):
        return "3DS "+self.consoleid

class User(AbstractUser):
    linked_ds = models.ForeignKey(Client3DS, null=True, on_delete=models.CASCADE)

class customTitleID(models.Model):
    tid = models.CharField(max_length=18, null=False)
    related_to = models.ForeignKey(Client3DS, null=False, on_delete=models.CASCADE)
    def __str__(self):
        return "Title "+self.tid+" for user "+self.related_to.consoleid

class age(models.Model): 
    name = models.CharField(max_length=20)
    parental_system_name = models.CharField(max_length=10)
    parental_system_id = models.IntegerField()
    icon_url_normal = models.URLField()
    icon_url_small = models.URLField()
    age_number = models.IntegerField(default=0)
    age_name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class descriptor(models.Model):
    name = models.CharField(max_length=100)
    icon_url_normal = models.URLField(blank=True)
    icon_url_small = models.URLField(blank=True)
    def __str__(self):
        return self.name

class publisher(models.Model):
    publisher_name = models.CharField(max_length=400)
    def __str__(self):
        return self.publisher_name

class category(models.Model):
    index = models.IntegerField(default=0, null=False)
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=250)
    standard = models.BooleanField(default=False)
    icon_url = models.URLField(null=False)
    banner_url = models.URLField(null=False)
    new = models.BooleanField(default=True)
    isagame = models.BooleanField(default=False)
    gameid = models.CharField(max_length=16, null=False)
    order = models.IntegerField(default=0)
    def __str__(self):
        return "Category "+self.name

class genre(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class feature(models.Model):
    type_number = models.IntegerField(blank=False, primary_key=False, serialize=False)
    name = models.CharField(max_length=75)
    icon_url_normal = models.URLField(blank=True)
    icon_url_small = models.URLField(blank=True)
    required = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class keyword(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class language(models.Model):
    iso_code = models.CharField(max_length=2)
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class website(models.Model):    
    name = models.CharField(max_length=150)
    website_name = models.CharField(max_length=110)
    url = models.URLField()
    official = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class platform(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Title(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    tid = models.CharField(max_length=16, null=False)
    name = models.CharField(max_length=150)
    age = models.ForeignKey(age, on_delete=models.CASCADE)
    descriptor = models.ManyToManyField('descriptor', blank=True)
    desc = models.TextField(default='', blank=True, null=True)
    disclaimer = models.TextField(default='', blank=True, null=True)
    thumbnail_url = models.TextField(max_length=10000, null=False)
    top_image_url = models.CharField(max_length=600, default='', blank=True, null=True)
    screenshot_upper_url = models.TextField(max_length=10000, default='', blank=True, null=True)
    screenshot_lower_url = models.TextField(max_length=10000, default='', blank=True, null=True)
    screenshot_merged_url = models.TextField(max_length=10000, default='', blank=True, null=True)
    icon_url = models.URLField(max_length=600, null=False)
    banner_url = models.URLField(max_length=600, null=False)
    publisher = models.ForeignKey(publisher, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, null=False)
    product_code = models.CharField(max_length=30)
    new = models.BooleanField(default=True)
    public = models.BooleanField(default=True)
    category = models.ForeignKey(category, on_delete=models.DO_NOTHING, null=True, blank=True)
    genre = models.ManyToManyField('genre')
    language = models.ManyToManyField('language', blank=True)
    number_of_players = models.CharField(max_length=6000, blank=True, null=True)
    website = models.ForeignKey(website, on_delete=models.CASCADE)
    copyright = models.CharField(max_length=15000, blank=True, null=True)
    in_app_purchase = models.BooleanField(default=False)
    platform = models.ForeignKey(platform, null=False, on_delete=models.CASCADE)
    price = models.IntegerField(default=0, null=False)
    version = models.IntegerField(default=1024)
    is_not_downloadable = models.BooleanField(default=False)
    size = models.IntegerField(default=0)
    ticket_available = models.BooleanField(default=True)
    demo = models.ForeignKey("title", on_delete=models.DO_NOTHING, null=True, blank=True)
    keyword = models.ManyToManyField('keyword', blank=True)
    feature = models.ManyToManyField('feature', blank=True)
    target_player_everyone = models.IntegerField(null=True, blank=True)
    target_player_gamers = models.IntegerField(null=True, blank=True)
    play_style_casual = models.IntegerField(null=True, blank=True)
    play_style_intense = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.name+" by "+self.publisher.publisher_name+" published on "+str(self.date)  

class item(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    title = models.ForeignKey(Title, null=False, on_delete=models.CASCADE)
    itemcode = models.CharField(max_length=16)
    price = models.IntegerField(default=0, null=False)
    limit = models.IntegerField(default=1, null=False)
    def __str__(self):
        return "Item "+str(self.id)+" for "+self.title.name

class movie(models.Model):
    name = models.CharField(max_length=500)
    thumbnail_url = models.URLField(max_length=600, null=False)
    banner_url = models.URLField(max_length=600, null=False)
    is_3d = models.BooleanField(default=False)
    moflex_url = models.URLField(max_length=1000, null=False)
    time_in_sec = models.IntegerField(null=False)
    date = models.DateField(auto_now_add=True, null=False)
    category = models.ForeignKey(category, on_delete=models.DO_NOTHING, null=True, blank=True)
    new = models.BooleanField(default=True, null=False)
    def __str__(self):
        return self.name

class ownedTitle(models.Model):
    title = models.ForeignKey(Title, null=False, on_delete=models.CASCADE)
    ticketid = models.CharField(max_length=16, null=False)
    version = models.IntegerField(null=False)
    owner = models.ForeignKey(Client3DS, null=False, on_delete=models.CASCADE)
    def __str__(self):
        return "Title "+self.title.name+" owned by "+self.owner.consoleid

class ownedTicket(models.Model):
    item = models.ForeignKey(item, null=False, on_delete=models.CASCADE)
    ticketid = models.CharField(max_length=16, null=False)
    owner = models.ForeignKey(Client3DS, null=False, on_delete=models.CASCADE)
    def __str__(self):
        return "Ticket "+self.item.itemcode+" owned by "+self.owner.consoleid

class wishlistedTitle(models.Model):
    title = models.ForeignKey(Title, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(Client3DS, null=False, on_delete=models.CASCADE)
    def __str__(self):
        return "Wishlisted title "+self.title.name+" wanted by "+self.owner.consoleid

class announcement(models.Model):
    title = models.CharField(max_length=60, null=False)
    content = models.TextField(null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)
    is_banner = models.BooleanField(default=False)
    banner_url = models.URLField(max_length=600, null=True, blank=True)
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
    name = models.CharField(max_length=35)
    platform_list = models.TextField(verbose_name="Platform List (seperate each platform by a comma)")
    def __str__(self):
        return self.name

class Vote(models.Model):
    client = models.ForeignKey(Client3DS, on_delete=models.CASCADE)
    voted_title = models.ForeignKey(Title, on_delete=models.CASCADE, null=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    q3 = models.CharField(max_length=10)
    q4 = models.BooleanField()
    q5 = models.BooleanField()
