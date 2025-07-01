from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class CompanyProfile(models.Model):
    """Model for company information and settings"""
    name = models.CharField(max_length=100, default="NUPO Consult Ltd")
    tagline = models.CharField(max_length=200, default="Rwanda's Engineering Partner")
    description = models.TextField(default="")
    phone = models.CharField(max_length=20, default="")
    email = models.EmailField(default="info@nupoconsult.com")
    address = models.TextField(default="")
    working_hours = models.CharField(max_length=100, default="Mon - Fri: 8:00 AM - 6:00 PM")
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Company Profiles"

    def __str__(self):
        return self.name


class CompanyStats(models.Model):
    """Model for company statistics displayed on homepage"""
    years_experience = models.IntegerField(default=10)
    projects_completed = models.IntegerField(default=150)
    happy_clients = models.IntegerField(default=50)
    support_hours = models.IntegerField(default=24)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Statistics"
        verbose_name_plural = "Company Statistics"

    def __str__(self):
        return f"Stats - {self.years_experience} years, {self.projects_completed} projects"


class ServiceCategory(models.Model):
    """Model for service categories"""
    name = models.CharField(max_length=100, default="General Services")
    slug = models.SlugField(unique=True, default="general-services")
    description = models.TextField(blank=True, default="")
    icon_class = models.CharField(max_length=50, default="fas fa-cog", help_text="FontAwesome icon class (e.g., 'fas fa-search')")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})


class Service(models.Model):
    """Model for individual services"""
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services', null=True, blank=True)
    title = models.CharField(max_length=200, default="Service Title")
    slug = models.SlugField(unique=True, default="service-slug")
    short_description = models.TextField(max_length=300, default="")
    full_description = models.TextField(default="")
    icon_class = models.CharField(max_length=50, default="fas fa-cog", help_text="FontAwesome icon class")
    features = models.JSONField(default=list, blank=True, help_text="List of service features")
    price_range = models.CharField(max_length=100, blank=True, default="")
    duration = models.CharField(max_length=100, blank=True, default="")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    meta_title = models.CharField(max_length=200, blank=True, default="")
    meta_description = models.CharField(max_length=300, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})


class TeamMember(models.Model):
    """Model for team members"""
    POSITION_CHOICES = [
        ('ceo', 'Chief Executive Officer'),
        ('director', 'Director'),
        ('manager', 'Manager'),
        ('engineer', 'Engineer'),
        ('consultant', 'Consultant'),
        ('supervisor', 'Supervisor'),
        ('specialist', 'Specialist'),
    ]

    name = models.CharField(max_length=100, default="Team Member")
    slug = models.SlugField(unique=True, default="team-member")
    position = models.CharField(max_length=200, default="Team Member")
    position_type = models.CharField(max_length=20, choices=POSITION_CHOICES, default='engineer')
    bio = models.TextField(default="")
    short_bio = models.TextField(max_length=300, default="")
    qualifications = models.TextField(blank=True, default="")
    experience_years = models.IntegerField(default=0)
    specializations = models.JSONField(default=list, blank=True)
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=20, blank=True, default="")
    linkedin_url = models.URLField(blank=True, default="")
    profile_image = models.ImageField(upload_to='team/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.position}"

    def get_absolute_url(self):
        return reverse('team_member_detail', kwargs={'slug': self.slug})


class Partner(models.Model):
    """Model for company partners"""
    PARTNER_TYPES = [
        ('government', 'Government Agency'),
        ('private', 'Private Sector'),
        ('ngo', 'NGO/Non-Profit'),
        ('academic', 'Academic Institution'),
        ('international', 'International Organization'),
        ('supplier', 'Supplier/Vendor'),
    ]

    name = models.CharField(max_length=100, default="Partner Name")
    slug = models.SlugField(unique=True, default="partner-slug")
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPES, default='private')
    description = models.TextField(blank=True, default="")
    logo = models.ImageField(upload_to='partners/', blank=True, null=True)
    website_url = models.URLField(blank=True, default="")
    partnership_start_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    """Model for news articles and updates"""
    ARTICLE_TYPES = [
        ('news', 'Company News'),
        ('award', 'Awards & Recognition'),
        ('project', 'Project Updates'),
        ('industry', 'Industry Insights'),
        ('sustainability', 'Sustainability'),
        ('training', 'Training & Education'),
    ]

    title = models.CharField(max_length=200, default="News Article")
    slug = models.SlugField(unique=True, default="news-article")
    article_type = models.CharField(max_length=20, choices=ARTICLE_TYPES, default='news')
    excerpt = models.TextField(max_length=300, default="")
    content = models.TextField(default="")
    featured_image = models.ImageField(upload_to='news/', blank=True, null=True)
    icon_class = models.CharField(max_length=50, default='fas fa-newspaper')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField(default=timezone.now)
    meta_title = models.CharField(max_length=200, blank=True, default="")
    meta_description = models.CharField(max_length=300, blank=True, default="")
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class Project(models.Model):
    """Model for company projects"""
    PROJECT_STATUS = [
        ('planning', 'Planning'),
        ('design', 'Design Phase'),
        ('construction', 'Under Construction'),
        ('completed', 'Completed'),
        ('maintenance', 'Maintenance Phase'),
    ]

    PROJECT_TYPES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('infrastructure', 'Infrastructure'),
        ('institutional', 'Institutional'),
    ]

    name = models.CharField(max_length=200, default="Project Name")
    slug = models.SlugField(unique=True, default="project-slug")
    client = models.CharField(max_length=100, default="Client Name")
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='commercial')
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='planning')
    description = models.TextField(default="")
    location = models.CharField(max_length=100, default="")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    services_provided = models.ManyToManyField(Service, blank=True)
    team_members = models.ManyToManyField(TeamMember, blank=True)
    featured_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    gallery_images = models.JSONField(default=list, blank=True)
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} - {self.client}"

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})


class ContactInquiry(models.Model):
    """Model for contact form submissions"""
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('quote', 'Request Quote'),
        ('consultation', 'Consultation Request'),
        ('partnership', 'Partnership Inquiry'),
        ('career', 'Career Inquiry'),
        ('complaint', 'Complaint'),
    ]

    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='general')
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    name = models.CharField(max_length=100, default="")
    email = models.EmailField(default="")
    phone = models.CharField(max_length=20, blank=True, default="")
    company = models.CharField(max_length=100, blank=True, default="")
    subject = models.CharField(max_length=200, default="")
    message = models.TextField(default="")
    services_interested = models.ManyToManyField(Service, blank=True)
    project_budget = models.CharField(max_length=100, blank=True, default="")
    project_timeline = models.CharField(max_length=100, blank=True, default="")
    is_responded = models.BooleanField(default=False)
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    response_date = models.DateTimeField(null=True, blank=True)
    response_notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Newsletter(models.Model):
    """Model for newsletter subscriptions"""
    email = models.EmailField(unique=True, default="")
    name = models.CharField(max_length=100, blank=True, default="")
    is_active = models.BooleanField(default=True)
    subscribed_date = models.DateTimeField(auto_now_add=True)
    unsubscribed_date = models.DateTimeField(null=True, blank=True)
    preferences = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
        ordering = ['-subscribed_date']

    def __str__(self):
        return self.email


class Testimonial(models.Model):
    """Model for client testimonials"""
    client_name = models.CharField(max_length=100, default="")
    client_company = models.CharField(max_length=100, blank=True, default="")
    client_position = models.CharField(max_length=100, blank=True, default="")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(default="")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    client_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.rating} stars"


class SEOSettings(models.Model):
    """Model for SEO settings per page"""
    page_name = models.CharField(max_length=50, unique=True, default="home")
    meta_title = models.CharField(max_length=200, default="")
    meta_description = models.CharField(max_length=300, default="")
    meta_keywords = models.CharField(max_length=500, blank=True, default="")
    og_title = models.CharField(max_length=200, blank=True, default="")
    og_description = models.CharField(max_length=300, blank=True, default="")
    og_image = models.ImageField(upload_to='seo/', blank=True, null=True)
    canonical_url = models.URLField(blank=True, default="")
    robots_meta = models.CharField(max_length=100, default='index, follow')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SEO Setting"
        verbose_name_plural = "SEO Settings"

    def __str__(self):
        return f"SEO - {self.page_name}"