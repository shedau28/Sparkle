
from email.policy import default
from django.db import models
# from django.contrib.auth.models import User

# Create your models here.


class Master(models.Model):
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    f_name = models.CharField(max_length=20)
    location = models.CharField(max_length=30)
    profile_pic = models.ImageField(upload_to='profile_images', default="blank_profile_picture.png")

    def __str__(self) -> str:
        return self.email

class Service(models.Model):
    # service_id = models.AutoField
    service_name = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    service_price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.id)


class OrderedService(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.id)


class Transaction(models.Model):
    made_by = models.CharField(max_length=10)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
