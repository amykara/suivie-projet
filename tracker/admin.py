from django.contrib import admin
from .models import Goal, SavingsConfig, SavingsEntry, Opportunity

admin.site.register(Goal)
admin.site.register(SavingsConfig)
admin.site.register(SavingsEntry)
admin.site.register(Opportunity)
