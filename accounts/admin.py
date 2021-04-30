from django.contrib import admin
from .models import Docitems, Document, editRecord
# Register your models here.
admin.site.register(Document)
admin.site.register(Docitems)
admin.site.register(editRecord)