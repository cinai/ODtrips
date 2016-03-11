from django.contrib import admin

from .models import *
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Transaction, TransactionAdmin)
