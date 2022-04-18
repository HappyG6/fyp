from django.db import models
# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    def __str__(self):
        return self.name

class Pdf(models.Model):
    name = models.CharField(max_length = 100)
    role = models.CharField(max_length = 100)
    datestart = models.CharField(max_length = 100)
    dateend = models.CharField(max_length = 100)
    def __str__(self):
        return self.name

class Certificate(models.Model):
    name= models.CharField(max_length=100 ,default="ok")
    pdf= models.FileField(upload_to='pdfs/', null=True, blank=True)
    hash= models.CharField(max_length=300 ,default="ok")
    web= models.CharField(max_length=1000,default="ok")
    # upload_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
