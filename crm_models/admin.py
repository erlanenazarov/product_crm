from django.contrib import admin
from models import *


# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = 'user_id order_id'.split()


admin.site.register(Orders)
admin.site.register(Client)
admin.site.register(OrderComment, CommentAdmin)
admin.site.register(Tag)
