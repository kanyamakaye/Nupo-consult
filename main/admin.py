from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db import models
from django.forms import Textarea
from .models import (
    CompanyProfile, CompanyStats, ServiceCategory, Service, TeamMember,
    Partner, NewsArticle, Project, ContactInquiry, Newsletter, Testimonial, SEOSettings
)

# Custom Admin Site Configuration
admin.site.site_header = "NUPO Consult Admin Dashboard"
admin.site.site_title = "NUPO Admin"
admin.site.index_title = "Welcome to NUPO Consult Administration"

class BaseModelAdmin(admin.ModelAdmin):
    """Base admin class with common functionality"""
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if hasattr(self.model, 'created_at'):
            readonly_fields.extend(['created_at', 'updated_at'])
        return readonly_fields

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if hasattr(self.model, 'created_at') and 'created_at' not in list_display:
            list_display.append('created_at')
        return list_display

@admin.register(CompanyProfile)
class CompanyProfileAdmin(BaseModelAdmin):
    list_display = ['name', 'tagline', 'email', 'phone', 'created_at']
    search_fields = ['name', 'tagline', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'tagline', 'description', 'logo')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address', 'working_hours')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        # Only allow one company profile
        return not CompanyProfile.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of company profile
        return False

@admin.register(CompanyStats)
class CompanyStatsAdmin(BaseModelAdmin):
    list_display = ['years_experience', 'projects_completed', 'happy_clients', 'support_hours', 'updated_at']
    
    fieldsets = (
        ('Statistics', {
            'fields': ('years_experience', 'projects_completed', 'happy_clients', 'support_hours')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        # Only allow one stats record
        return not CompanyStats.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(BaseModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order', 'service_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'icon_class')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def service_count(self, obj):
        count = obj.services.count()
        if count > 0:
            url = reverse('admin:main_service_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} services</a>', url, count)
        return '0 services'
    service_count.short_description = 'Services'

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0
    fields = ['title', 'slug', 'is_active', 'is_featured', 'order']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Service)
class ServiceAdmin(BaseModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'is_active', 'price_range', 'order', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'short_description', 'full_description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_active', 'order']
    ordering = ['category', 'order', 'title']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'slug', 'icon_class')
        }),
        ('Content', {
            'fields': ('short_description', 'full_description', 'features')
        }),
        ('Pricing & Duration', {
            'fields': ('price_range', 'duration')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    formfield_overrides = {
        models.JSONField: {'widget': Textarea(attrs={'rows': 4, 'cols': 80})},
    }
    
    actions = ['make_featured', 'remove_featured', 'activate', 'deactivate']
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} services marked as featured.")
    make_featured.short_description = "Mark selected services as featured"
    
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} services removed from featured.")
    remove_featured.short_description = "Remove selected services from featured"
    
    def activate(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} services activated.")
    activate.short_description = "Activate selected services"
    
    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} services deactivated.")
    deactivate.short_description = "Deactivate selected services"

@admin.register(TeamMember)
class TeamMemberAdmin(BaseModelAdmin):
    list_display = ['name', 'position', 'position_type', 'experience_years', 'is_featured', 'is_active', 'profile_image_preview']
    list_filter = ['position_type', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'position', 'bio', 'qualifications']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'position', 'position_type', 'profile_image')
        }),
        ('Biography', {
            'fields': ('bio', 'short_bio', 'qualifications', 'experience_years', 'specializations')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'linkedin_url'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    formfield_overrides = {
        models.JSONField: {'widget': Textarea(attrs={'rows': 3, 'cols': 80})},
    }
    
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', obj.profile_image.url)
        return "No Image"
    profile_image_preview.short_description = 'Profile Image'
    
    actions = ['make_featured', 'remove_featured']
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} team members marked as featured.")
    make_featured.short_description = "Mark selected team members as featured"
    
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} team members removed from featured.")
    remove_featured.short_description = "Remove selected team members from featured"

@admin.register(Partner)
class PartnerAdmin(BaseModelAdmin):
    list_display = ['name', 'partner_type', 'is_featured', 'is_active', 'partnership_start_date', 'logo_preview']
    list_filter = ['partner_type', 'is_featured', 'is_active', 'partnership_start_date']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'partner_type', 'description', 'logo')
        }),
        ('Partnership Details', {
            'fields': ('website_url', 'partnership_start_date')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="30" style="object-fit: contain;" />', obj.logo.url)
        return "No Logo"
    logo_preview.short_description = 'Logo'

@admin.register(NewsArticle)
class NewsArticleAdmin(BaseModelAdmin):
    list_display = ['title', 'article_type', 'author', 'is_featured', 'is_published', 'published_date', 'views_count']
    list_filter = ['article_type', 'is_featured', 'is_published', 'published_date', 'author']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_published']
    ordering = ['-published_date']
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'article_type', 'author')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image', 'icon_class')
        }),
        ('Publishing', {
            'fields': ('is_featured', 'is_published', 'published_date')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['publish', 'unpublish', 'make_featured']
    
    def publish(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} articles published.")
    publish.short_description = "Publish selected articles"
    
    def unpublish(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} articles unpublished.")
    unpublish.short_description = "Unpublish selected articles"
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} articles marked as featured.")
    make_featured.short_description = "Mark selected articles as featured"

class ProjectServiceInline(admin.TabularInline):
    model = Project.services_provided.through
    extra = 1
    verbose_name = "Service"
    verbose_name_plural = "Services Provided"

class ProjectTeamInline(admin.TabularInline):
    model = Project.team_members.through
    extra = 1
    verbose_name = "Team Member"
    verbose_name_plural = "Team Members"

@admin.register(Project)
class ProjectAdmin(BaseModelAdmin):
    list_display = ['name', 'client', 'project_type', 'status', 'start_date', 'end_date', 'is_featured', 'is_public']
    list_filter = ['project_type', 'status', 'is_featured', 'is_public', 'start_date']
    search_fields = ['name', 'client', 'description', 'location']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_public']
    ordering = ['-start_date']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'client', 'project_type', 'status')
        }),
        ('Project Details', {
            'fields': ('description', 'location', 'start_date', 'end_date', 'budget')
        }),
        ('Media', {
            'fields': ('featured_image', 'gallery_images')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_public')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    filter_horizontal = ['services_provided', 'team_members']
    
    formfield_overrides = {
        models.JSONField: {'widget': Textarea(attrs={'rows': 3, 'cols': 80})},
    }
    
    actions = ['make_featured', 'make_public', 'make_private']
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} projects marked as featured.")
    make_featured.short_description = "Mark selected projects as featured"
    
    def make_public(self, request, queryset):
        queryset.update(is_public=True)
        self.message_user(request, f"{queryset.count()} projects made public.")
    make_public.short_description = "Make selected projects public"
    
    def make_private(self, request, queryset):
        queryset.update(is_public=False)
        self.message_user(request, f"{queryset.count()} projects made private.")
    make_private.short_description = "Make selected projects private"

@admin.register(ContactInquiry)
class ContactInquiryAdmin(BaseModelAdmin):
    list_display = ['name', 'email', 'inquiry_type', 'priority', 'subject', 'is_responded', 'created_at']
    list_filter = ['inquiry_type', 'priority', 'is_responded', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message', 'company']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['priority', 'is_responded']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Inquiry Details', {
            'fields': ('inquiry_type', 'priority', 'subject', 'message')
        }),
        ('Project Information', {
            'fields': ('services_interested', 'project_budget', 'project_timeline'),
            'classes': ('collapse',)
        }),
        ('Response', {
            'fields': ('is_responded', 'responded_by', 'response_date', 'response_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    filter_horizontal = ['services_interested']
    
    actions = ['mark_responded', 'mark_unresponded', 'set_high_priority']
    
    def mark_responded(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_responded=True, responded_by=request.user, response_date=timezone.now())
        self.message_user(request, f"{queryset.count()} inquiries marked as responded.")
    mark_responded.short_description = "Mark selected inquiries as responded"
    
    def mark_unresponded(self, request, queryset):
        queryset.update(is_responded=False, responded_by=None, response_date=None)
        self.message_user(request, f"{queryset.count()} inquiries marked as unresponded.")
    mark_unresponded.short_description = "Mark selected inquiries as unresponded"
    
    def set_high_priority(self, request, queryset):
        queryset.update(priority='high')
        self.message_user(request, f"{queryset.count()} inquiries set to high priority.")
    set_high_priority.short_description = "Set selected inquiries to high priority"

@admin.register(Newsletter)
class NewsletterAdmin(BaseModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_date', 'unsubscribed_date']
    list_filter = ['is_active', 'subscribed_date', 'unsubscribed_date']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_date', 'unsubscribed_date']
    list_editable = ['is_active']
    ordering = ['-subscribed_date']
    date_hierarchy = 'subscribed_date'
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'name', 'is_active')
        }),
        ('Preferences', {
            'fields': ('preferences',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('subscribed_date', 'unsubscribed_date'),
            'classes': ('collapse',)
        })
    )
    
    formfield_overrides = {
        models.JSONField: {'widget': Textarea(attrs={'rows': 3, 'cols': 80})},
    }
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        queryset.update(is_active=True, unsubscribed_date=None)
        self.message_user(request, f"{queryset.count()} subscriptions activated.")
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_active=False, unsubscribed_date=timezone.now())
        self.message_user(request, f"{queryset.count()} subscriptions deactivated.")
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"

@admin.register(Testimonial)
class TestimonialAdmin(BaseModelAdmin):
    list_display = ['client_name', 'client_company', 'rating', 'is_featured', 'is_approved', 'project', 'service']
    list_filter = ['rating', 'is_featured', 'is_approved', 'created_at']
    search_fields = ['client_name', 'client_company', 'content']
    list_editable = ['is_featured', 'is_approved']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_company', 'client_position', 'client_photo')
        }),
        ('Testimonial', {
            'fields': ('content', 'rating', 'project', 'service')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_approved')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['approve', 'unapprove', 'make_featured']
    
    def approve(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} testimonials approved.")
    approve.short_description = "Approve selected testimonials"
    
    def unapprove(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} testimonials unapproved.")
    unapprove.short_description = "Unapprove selected testimonials"
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} testimonials marked as featured.")
    make_featured.short_description = "Mark selected testimonials as featured"

@admin.register(SEOSettings)
class SEOSettingsAdmin(BaseModelAdmin):
    list_display = ['page_name', 'meta_title', 'meta_description', 'updated_at']
    search_fields = ['page_name', 'meta_title', 'meta_description']
    
    fieldsets = (
        ('Page Information', {
            'fields': ('page_name',)
        }),
        ('Meta Tags', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Open Graph', {
            'fields': ('og_title', 'og_description', 'og_image'),
            'classes': ('collapse',)
        }),
        ('Advanced SEO', {
            'fields': ('canonical_url', 'robots_meta'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

# Custom Admin Dashboard
class AdminDashboard:
    """Custom admin dashboard with statistics"""
    
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)
        
        # Add custom statistics
        if app_dict:
            for app in app_dict:
                if app['app_label'] == 'main':
                    app['models'].insert(0, {
                        'name': 'Dashboard Statistics',
                        'object_name': 'Statistics',
                        'admin_url': '/admin/dashboard-stats/',
                        'add_url': None,
                        'view_only': True,
                    })
        
        return app_dict

# Register custom admin site
admin.site.__class__ = type('CustomAdminSite', (admin.site.__class__, AdminDashboard), {})
