from django.contrib import admin
from .models import Category, Question, UserScore
from .models import  FAQ
# Register models
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(UserScore)
admin.site.register(FAQ)
