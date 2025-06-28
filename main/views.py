from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Service, TeamMember, Newsletter, ContactMessage
import json

def home(request):
    services = Service.objects.all()[:6]  # Show first 6 services
    team_members = TeamMember.objects.all()[:2]  # Show key team members
    context = {
        'services': services,
        'team_members': team_members,
    }
    return render(request, 'main/home.html', context)

def about(request):
    team_members = TeamMember.objects.all()
    context = {
        'team_members': team_members,
    }
    return render(request, 'main/about.html', context)

def services(request):
    services = Service.objects.all()
    context = {
        'services': services,
    }
    return render(request, 'main/services.html', context)

def news(request):
    # You can add a News model later and display articles here
    return render(request, 'main/news.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save to database
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Send email notification (optional)
        try:
            send_mail(
                f'New Contact Message: {subject}',
                f'From: {name} ({email})\n\nMessage:\n{message}',
                settings.EMAIL_HOST_USER,
                ['info@nupoconsult.com'],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('main:contact')
    
    return render(request, 'main/contact.html')

def newsletter_subscribe(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                email = data.get('email')
            else:
                email = request.POST.get('email')
            
            if email:
                newsletter, created = Newsletter.objects.get_or_create(
                    email=email,
                    defaults={'is_active': True}
                )
                
                if created:
                    return JsonResponse({'success': True, 'message': 'Successfully subscribed to newsletter!'})
                else:
                    return JsonResponse({'success': False, 'message': 'Email already subscribed!'})
            else:
                return JsonResponse({'success': False, 'message': 'Email is required!'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method!'})


def team_list(request):
    team_members = TeamMember.objects.all()
    return render(request, 'team/team_list.html', {'team_members': team_members})
from .models import Partner

def partners_view(request):
    partners = Partner.objects.all()
    return render(request, 'team/partners.html', {'partners': partners})


def feasibility_view(request):
    return render(request, 'main/feasibility.html')

def design_more(request):
    return render(request, 'main/designs.html')

def analysis_more(request):
    return render(request, 'main/Analysis.html')
def engineering_more(request):
    return render(request, 'main/Engineering.html')
def permitting_more(request):
    return render(request, 'main/Permit.html')
def construction_more(request):
    return render(request, 'main/Construction.html')
def engineering_more(request):
    return render(request, 'main/Engineering.html')
