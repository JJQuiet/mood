from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL # django 内置对象

# Create your models here.
class Document(models.Model):
    file = models.FileField(upload_to='csv')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)

class Docitems(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    editor1 = models.CharField(max_length=35, null=True, blank=True)
    editor2 = models.CharField(max_length=35, null=True, blank=True)
    editor3 = models.CharField(max_length=35, null=True, blank=True)
    review = models.TextField(max_length=1000)
    label1 = models.IntegerField(default=2)
    label2 = models.IntegerField(default=2)
    label3 = models.IntegerField(default=2)
    label = models.IntegerField(default=2)
    last_edit_time = models.DateTimeField(auto_now_add=True)
    @property
    def mylabel(self):
        return self.label
    @mylabel.setter
    def mylabel(self,value):
        if self.label1 == self.label2 or self.label1 == self.label3 or self.label2 == self.label3 :
            if self.label1 == self.label2:
                self.label = self.label1
            if self.label1 == self.label3:
                self.label = self.label1
            if self.label2 == self.label3:
                self.label = self.label2
    def calculabel(self):
        if self.label1 == self.label2 or self.label1 == self.label3 or self.label2 == self.label3 :
            if self.label1 == self.label2:
                return self.label1
            if self.label1 == self.label3:
                return self.label1
            if self.label2 == self.label3:
                return self.label2
class editRecord(models.Model):
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(Document, on_delete=models.CASCADE)
    last_edit_row = models.IntegerField(default=0)