from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import (
    CompanyProfile, CompanyStats, ServiceCategory, Service, TeamMember,
    Partner, NewsArticle, Project, ContactInquiry, Newsletter, Testimonial, SEOSettings
)

def get_company_context():
    """Get common company data for all views"""
    try:
        company = CompanyProfile.objects.first()
        stats = CompanyStats.objects.first()
    except:
        company = None
        stats = None
    
    return {
        'company': company,
        'stats': stats,
    }

def home(request):
    """Homepage view"""
    context = get_company_context()
    
    # Get featured content
    context.update({
        'featured_services': Service.objects.filter(is_featured=True, is_active=True)[:6],
        'featured_projects': Project.objects.filter(is_featured=True, is_public=True)[:3],
        'featured_testimonials': Testimonial.objects.filter(is_featured=True, is_approved=True)[:3],
        'recent_news': NewsArticle.objects.filter(is_published=True)[:3],
        'partners': Partner.objects.filter(is_active=True)[:8],
        'team_members': TeamMember.objects.filter(is_featured=True, is_active=True)[:4],
    })
    
    # SEO
    try:
        seo = SEOSettings.objects.get(page_name='home')
        context['seo'] = seo
    except SEOSettings.DoesNotExist:
        pass
    
    return render(request, 'home.html', context)

def services(request):
    """Services listing page"""
    context = get_company_context()
    
    categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services')
    services_list = Service.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        services_list = services_list.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    context.update({
        'categories': categories,
        'services': services_list,
        'search_query': search_query,
    })
    
    return render(request, 'services.html', context)

def service_detail(request, slug):
    """Service detail page"""
    context = get_company_context()
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    # Related services
    related_services = Service.objects.filter(
        category=service.category, is_active=True
    ).exclude(id=service.id)[:3]
    
    context.update({
        'service': service,
        'related_services': related_services,
    })
    
    return render(request, 'service_detail.html', context)

def team(request):
    """Team page"""
    context = get_company_context()
    
    team_members = TeamMember.objects.filter(is_active=True)
    
    context.update({
        'team_members': team_members,
    })
    
    return render(request, 'team.html', context)

def projects(request):
    """Projects/Portfolio page"""
    context = get_company_context()
    
    projects_list = Project.objects.filter(is_public=True)
    
    # Filter by type
    project_type = request.GET.get('type', '')
    if project_type:
        projects_list = projects_list.filter(project_type=project_type)
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        projects_list = projects_list.filter(status=status)
    
    # Pagination
    paginator = Paginator(projects_list, 9)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    context.update({
        'projects': projects,
        'project_types': Project.PROJECT_TYPES,
        'project_statuses': Project.PROJECT_STATUS,
        'selected_type': project_type,
        'selected_status': status,
    })
    
    return render(request, 'projects.html', context)

def project_detail(request, slug):
    """Project detail page"""
    context = get_company_context()
    project = get_object_or_404(Project, slug=slug, is_public=True)
    
    context.update({
        'project': project,
    })
    
    return render(request, 'project_detail.html', context)

def news(request):
    """News/Blog listing page"""
    context = get_company_context()
    
    articles_list = NewsArticle.objects.filter(is_published=True)
    
    # Filter by type
    article_type = request.GET.get('type', '')
    if article_type:
        articles_list = articles_list.filter(article_type=article_type)
    
    # Pagination
    paginator = Paginator(articles_list, 6)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    
    context.update({
        'articles': articles,
        'article_types': NewsArticle.ARTICLE_TYPES,
        'selected_type': article_type,
        'featured_articles': NewsArticle.objects.filter(is_featured=True, is_published=True)[:3],
    })
    
    return render(request, 'news.html', context)

def news_detail(request, slug):
    """News article detail page"""
    context = get_company_context()
    article = get_object_or_404(NewsArticle, slug=slug, is_published=True)
    
    # Increment views
    article.increment_views()
    
    # Related articles
    related_articles = NewsArticle.objects.filter(
        article_type=article.article_type, is_published=True
    ).exclude(id=article.id)[:3]
    
    context.update({
        'article': article,
        'related_articles': related_articles,
    })
    
    return render(request, 'news_detail.html', context)

def about(request):
    """About page"""
    context = get_company_context()
    
    context.update({
        'team_members': TeamMember.objects.filter(is_active=True)[:8],
        'partners': Partner.objects.filter(is_active=True),
    })
    
    return render(request, 'about.html', context)

def contact(request):
    """Contact page"""
    context = get_company_context()
    
    if request.method == 'POST':
        # Handle contact form submission
        try:
            inquiry = ContactInquiry(
                inquiry_type=request.POST.get('inquiry_type', 'general'),
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone', ''),
                company=request.POST.get('company', ''),
                subject=request.POST.get('subject'),
                message=request.POST.get('message'),
                project_budget=request.POST.get('budget', ''),
                project_timeline=request.POST.get('timeline', ''),
            )
            inquiry.save()
            
            # Add selected services
            services = request.POST.getlist('services')
            if services:
                inquiry.services_interested.set(services)
            
            messages.success(request, 'Thank you for your inquiry! We will get back to you soon.')
            return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, 'There was an error submitting your inquiry. Please try again.')
            return JsonResponse({'success': False, 'error': str(e)})
    
    context.update({
        'services': Service.objects.filter(is_active=True),
        'inquiry_types': ContactInquiry.INQUIRY_TYPES,
    })
    
    return render(request, 'contact.html', context)

def newsletter_subscribe(request):
    """Newsletter subscription endpoint"""
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name', '')
        
        if email:
            newsletter, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={'name': name, 'is_active': True}
            )
            
            if created:
                return JsonResponse({'success': True, 'message': 'Successfully subscribed to newsletter!'})
            else:
                if newsletter.is_active:
                    return JsonResponse({'success': False, 'message': 'Email already subscribed.'})
                else:
                    newsletter.is_active = True
                    newsletter.save()
                    return JsonResponse({'success': True, 'message': 'Subscription reactivated!'})
        
        return JsonResponse({'success': False, 'message': 'Please provide a valid email address.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
