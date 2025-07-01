from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    CompanyProfile, CompanyStats, Service, TeamMember, Partner,
    NewsArticle, Project, ContactInquiry, Newsletter, Testimonial
)

@staff_member_required
def dashboard_stats(request):
    """Custom dashboard with statistics"""
    
    # Get date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Basic counts
    stats = {
        'services': {
            'total': Service.objects.count(),
            'active': Service.objects.filter(is_active=True).count(),
            'featured': Service.objects.filter(is_featured=True).count(),
        },
        'projects': {
            'total': Project.objects.count(),
            'public': Project.objects.filter(is_public=True).count(),
            'completed': Project.objects.filter(status='completed').count(),
            'in_progress': Project.objects.filter(status='construction').count(),
        },
        'team': {
            'total': TeamMember.objects.count(),
            'active': TeamMember.objects.filter(is_active=True).count(),
            'featured': TeamMember.objects.filter(is_featured=True).count(),
        },
        'content': {
            'news_articles': NewsArticle.objects.filter(is_published=True).count(),
            'testimonials': Testimonial.objects.filter(is_approved=True).count(),
            'partners': Partner.objects.filter(is_active=True).count(),
        },
        'inquiries': {
            'total': ContactInquiry.objects.count(),
            'this_week': ContactInquiry.objects.filter(created_at__gte=week_ago).count(),
            'this_month': ContactInquiry.objects.filter(created_at__gte=month_ago).count(),
            'unresponded': ContactInquiry.objects.filter(is_responded=False).count(),
            'high_priority': ContactInquiry.objects.filter(priority='high', is_responded=False).count(),
        },
        'newsletter': {
            'total_subscribers': Newsletter.objects.filter(is_active=True).count(),
            'new_this_week': Newsletter.objects.filter(subscribed_date__gte=week_ago).count(),
            'new_this_month': Newsletter.objects.filter(subscribed_date__gte=month_ago).count(),
        }
    }
    
    # Recent activities
    recent_inquiries = ContactInquiry.objects.order_by('-created_at')[:5]
    recent_subscribers = Newsletter.objects.order_by('-subscribed_date')[:5]
    recent_articles = NewsArticle.objects.filter(is_published=True).order_by('-published_date')[:5]
    
    # Inquiry types breakdown
    inquiry_types = ContactInquiry.objects.values('inquiry_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Project status breakdown
    project_status = Project.objects.values('status').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'stats': stats,
        'recent_inquiries': recent_inquiries,
        'recent_subscribers': recent_subscribers,
        'recent_articles': recent_articles,
        'inquiry_types': inquiry_types,
        'project_status': project_status,
        'title': 'Dashboard Statistics',
    }
    
    return render(request, 'admin/dashboard_stats.html', context)
