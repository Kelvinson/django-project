from django.contrib import admin
from .models import Post,FDataFrame,ADataFrame

# Register your models here.
admin.site.register(Post)
admin.site.register(FDataFrame)
admin.site.register(ADataFrame)

