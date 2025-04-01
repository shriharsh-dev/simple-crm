from django.contrib import admin
from .models import Customer, Interaction

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','company','status','created_at')
    list_filter = ('status','created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company')
    
@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('customer','interaction_type','subject','date')
    list_filter = ('interaction_type','date')
    search_fields = ('subject', 'notes')
