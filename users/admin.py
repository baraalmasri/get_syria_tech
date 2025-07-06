from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ['user', 'get_full_name', 'phone', 'city', 'country', 
                   'newsletter_subscription', 'created']
    list_filter = ['newsletter_subscription', 'sms_notifications', 'country', 'created']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 
                    'user__email', 'phone']
    list_per_page = 20
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'address', 'postal_code', 'city', 'country')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth',)
        }),
        ('Preferences', {
            'fields': ('newsletter_subscription', 'sms_notifications')
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

