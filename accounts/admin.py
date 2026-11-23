from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'approval_status', 'is_staff', 'created_at')
    list_filter = ('is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email')
    readonly_fields = ('created_at',)
    
    def approval_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✅ Approved</span>')
        else:
            return format_html('<span style="color: orange; font-weight: bold;">⏳ Pending Approval</span>')
    approval_status.short_description = 'Status'
    
    actions = ['approve_users']
    
    def approve_users(self, request, queryset):
        count = queryset.update(is_active=True)
        # Try to send email to approved users
        for user in queryset:
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                send_mail(
                    'Your account has been approved',
                    f'Hello {user.username},\n\nYour account has been approved by admin. You can now log in.\n\nLogin: https://myday.bdcrafter.com/accounts/login/',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True
                )
            except Exception:
                pass
        self.message_user(request, f'✅ {count} user(s) approved successfully!')
    approve_users.short_description = '✅ Approve selected users'
    
    fieldsets = UserAdmin.fieldsets + (
        ('Approval Info', {'fields': ('created_at',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')

admin.site.register(CustomUser, CustomUserAdmin)