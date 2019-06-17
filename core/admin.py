from django.contrib import admin
from core import models


admin.site.site_header = "Favorite_things Admin"
admin.site.site_title = "Favorite_things Admin Portal"
admin.site.index_title = "Welcome to Favorite_things Admin portal"

admin.site.register(models.User)
admin.site.register(models.Category)
