import os
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

# You'll need to import your models - adjust the import path as needed
from main.models import (
    CompanyProfile, CompanyStats, ServiceCategory, Service, TeamMember,
    Partner, NewsArticle, Project, ContactInquiry, Newsletter, Testimonial, SEOSettings
)

class Command(BaseCommand):
    help = 'Create sample data for the NUPO Consult website'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing data before creating new sample data',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Deleting existing data...')
            self.delete_existing_data()
        
        self.stdout.write('Creating sample data...')
        
        # Create company profile
        self.create_company_profile()
        
        # Create company stats
        self.create_company_stats()
        
        # Create service categories and services
        self.create_services()
        
        # Create team members
        self.create_team_members()
        
        # Create partners
        self.create_partners()
        
        # Create news articles
        self.create_news_articles()
        
        # Create projects
        self.create_projects()
        
        # Create testimonials
        self.create_testimonials()
        
        # Create sample inquiries
        self.create_sample_inquiries()
        
        # Create newsletter subscribers
        self.create_newsletter_subscribers()
        
        # Create SEO settings
        self.create_seo_settings()
        
        self.stdout.write(self.style.SUCCESS('✅ Sample data created successfully!'))
        self.stdout.write('You can now access the admin at /admin/ and the website at /')

    def delete_existing_data(self):
        """Delete existing data (except superuser)"""
        models_to_clear = [
            ContactInquiry, Newsletter, Testimonial, Project, NewsArticle,
            Partner, TeamMember, Service, ServiceCategory, SEOSettings,
            CompanyStats, CompanyProfile
        ]
        
        for model in models_to_clear:
            count = model.objects.count()
            model.objects.all().delete()
            self.stdout.write(f'  Deleted {count} {model._meta.verbose_name_plural}')

    def create_company_profile(self):
        company, created = CompanyProfile.objects.get_or_create(
            name="NUPO Consult Ltd",
            defaults={
                'tagline': "Rwanda's Engineering Partner",
                'description': """NUPO Consult Ltd is a leading engineering consultancy firm based in Kigali, Rwanda. 
                We specialize in providing innovative, sustainable, and cost-effective engineering solutions across 
                various sectors including infrastructure development, building construction, environmental engineering, 
                and project management. Our team of experienced professionals is committed to excellence and 
                contributing to Rwanda's sustainable development goals.""",
                'phone': "+250 788 123 456",
                'email': "info@nupoconsult.rw",
                'address': "KN 4 Ave, Nyarugenge District, Kigali City, Rwanda",
                'working_hours': "Monday - Friday: 8:00 AM - 6:00 PM, Saturday: 9:00 AM - 1:00 PM",
                'facebook_url': "https://facebook.com/nupoconsult",
                'linkedin_url': "https://linkedin.com/company/nupoconsult",
                'twitter_url': "https://twitter.com/nupoconsult",
                'instagram_url': "https://instagram.com/nupoconsult",
            }
        )
        if created:
            self.stdout.write('  ✓ Created company profile')
        else:
            self.stdout.write('  → Company profile already exists')

    def create_company_stats(self):
        stats, created = CompanyStats.objects.get_or_create(
            defaults={
                'years_experience': 12,
                'projects_completed': 185,
                'happy_clients': 67,
                'support_hours': 24,
            }
        )
        if created:
            self.stdout.write('  ✓ Created company statistics')
        else:
            self.stdout.write('  → Company statistics already exist')

    def create_services(self):
        # Create service categories
        categories_data = [
            {
                'name': 'Structural Engineering',
                'description': 'Comprehensive structural design and analysis services for buildings and infrastructure',
                'icon_class': 'fas fa-building'
            },
            {
                'name': 'Civil Engineering',
                'description': 'Road construction, water systems, and infrastructure development services',
                'icon_class': 'fas fa-road'
            },
            {
                'name': 'Project Management',
                'description': 'Professional project management and construction supervision services',
                'icon_class': 'fas fa-tasks'
            },
            {
                'name': 'Environmental Engineering',
                'description': 'Environmental impact assessments and sustainable engineering solutions',
                'icon_class': 'fas fa-leaf'
            },
            {
                'name': 'Consulting Services',
                'description': 'Expert consulting and feasibility studies for engineering projects',
                'icon_class': 'fas fa-handshake'
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description'],
                    'icon_class': cat_data['icon_class'],
                    'is_active': True,
                    'order': len(categories) + 1
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'  ✓ Created category: {cat_data["name"]}')

        # Create services
        services_data = [
            {
                'title': 'Building Structural Design',
                'category': 'Structural Engineering',
                'short_description': 'Complete structural design services for residential and commercial buildings',
                'full_description': 'Our structural engineering team provides comprehensive building design services including foundation design, structural analysis, and construction drawings for all types of buildings.',
                'price_range': '$5,000 - $50,000',
                'duration': '2-8 weeks',
                'features': ['Foundation Design', 'Structural Analysis', 'Construction Drawings', 'Building Permits Support']
            },
            {
                'title': 'Bridge Design & Analysis',
                'category': 'Structural Engineering',
                'short_description': 'Specialized bridge engineering and structural analysis services',
                'full_description': 'Expert bridge design services including structural analysis, load calculations, and detailed engineering drawings for various bridge types.',
                'price_range': '$15,000 - $100,000',
                'duration': '4-12 weeks',
                'features': ['Load Analysis', 'Structural Modeling', 'Construction Plans', 'Safety Assessments']
            },
            {
                'title': 'Road Construction & Design',
                'category': 'Civil Engineering',
                'short_description': 'Complete road infrastructure design and construction management',
                'full_description': 'Full-service road construction including surveying, design, construction supervision, and quality control for urban and rural road projects.',
                'price_range': '$20,000 - $500,000',
                'duration': '3-18 months',
                'features': ['Surveying', 'Pavement Design', 'Drainage Systems', 'Traffic Management']
            },
            {
                'title': 'Water Supply Systems',
                'category': 'Civil Engineering',
                'short_description': 'Design and installation of water supply and distribution systems',
                'full_description': 'Comprehensive water supply system design including source development, treatment, storage, and distribution networks for communities and institutions.',
                'price_range': '$10,000 - $200,000',
                'duration': '2-12 months',
                'features': ['Source Development', 'Treatment Design', 'Distribution Networks', 'Pump Stations']
            },
            {
                'title': 'Construction Project Management',
                'category': 'Project Management',
                'short_description': 'Professional construction project management and supervision services',
                'full_description': 'Complete project management services from planning to completion including scheduling, cost control, quality assurance, and stakeholder coordination.',
                'price_range': '5-10% of project cost',
                'duration': 'Project duration',
                'features': ['Project Planning', 'Cost Control', 'Quality Assurance', 'Progress Monitoring']
            },
            {
                'title': 'Engineering Supervision',
                'category': 'Project Management',
                'short_description': 'On-site engineering supervision and quality control services',
                'full_description': 'Professional engineering supervision services ensuring construction quality, safety compliance, and adherence to design specifications.',
                'price_range': '$2,000 - $10,000/month',
                'duration': 'Construction period',
                'features': ['Quality Control', 'Safety Monitoring', 'Progress Reports', 'Technical Support']
            },
            {
                'title': 'Environmental Impact Assessment',
                'category': 'Environmental Engineering',
                'short_description': 'Comprehensive environmental impact studies and mitigation planning',
                'full_description': 'Professional EIA services including baseline studies, impact prediction, mitigation measures, and environmental management plans.',
                'price_range': '$8,000 - $30,000',
                'duration': '6-16 weeks',
                'features': ['Baseline Studies', 'Impact Assessment', 'Mitigation Planning', 'Monitoring Programs']
            },
            {
                'title': 'Waste Management Systems',
                'category': 'Environmental Engineering',
                'short_description': 'Design of sustainable waste management and treatment systems',
                'full_description': 'Innovative waste management solutions including collection systems, treatment facilities, and recycling programs for communities and industries.',
                'price_range': '$15,000 - $100,000',
                'duration': '3-8 months',
                'features': ['Collection Systems', 'Treatment Design', 'Recycling Solutions', 'Monitoring Systems']
            },
            {
                'title': 'Feasibility Studies',
                'category': 'Consulting Services',
                'short_description': 'Comprehensive project feasibility analysis and planning services',
                'full_description': 'Detailed feasibility studies including technical, economic, and environmental analysis to support informed decision-making for engineering projects.',
                'price_range': '$5,000 - $25,000',
                'duration': '4-8 weeks',
                'features': ['Technical Analysis', 'Economic Evaluation', 'Risk Assessment', 'Recommendations']
            },
            {
                'title': 'Engineering Consulting',
                'category': 'Consulting Services',
                'short_description': 'Expert engineering consultation and technical advisory services',
                'full_description': 'Professional engineering consulting services providing technical expertise, problem-solving, and strategic advice for complex engineering challenges.',
                'price_range': '$150 - $300/hour',
                'duration': 'As required',
                'features': ['Technical Expertise', 'Problem Solving', 'Strategic Planning', 'Expert Testimony']
            }
        ]
        
        for service_data in services_data:
            category = categories[service_data['category']]
            service, created = Service.objects.get_or_create(
                title=service_data['title'],
                defaults={
                    'category': category,
                    'slug': slugify(service_data['title']),
                    'short_description': service_data['short_description'],
                    'full_description': service_data['full_description'],
                    'icon_class': 'fas fa-cogs',
                    'features': service_data['features'],
                    'price_range': service_data['price_range'],
                    'duration': service_data['duration'],
                    'is_active': True,
                    'is_featured': random.choice([True, False]),
                    'order': random.randint(1, 10)
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created service: {service_data["title"]}')

    def create_team_members(self):
        team_data = [
            {
                'name': 'Eng. Jean Baptiste UWIMANA',
                'position': 'Chief Executive Officer & Senior Engineer',
                'position_type': 'ceo',
                'bio': 'Jean Baptiste is a seasoned civil engineer with over 15 years of experience in infrastructure development across East Africa. He holds a Master\'s degree in Civil Engineering and has led numerous high-profile projects including road construction, bridge design, and urban planning initiatives.',
                'short_bio': 'Experienced CEO and Senior Civil Engineer with 15+ years in infrastructure development',
                'qualifications': 'MSc Civil Engineering, Professional Engineer (PE), Project Management Professional (PMP)',
                'experience_years': 15,
                'specializations': ['Infrastructure Development', 'Project Management', 'Urban Planning', 'Bridge Design'],
                'email': 'ceo@nupoconsult.rw',
                'linkedin_url': 'https://linkedin.com/in/jb-uwimana'
            },
            {
                'name': 'Eng. Marie MUKAMANA',
                'position': 'Senior Structural Engineer',
                'position_type': 'engineer',
                'bio': 'Marie is a highly skilled structural engineer specializing in building design and seismic analysis. With 12 years of experience, she has designed over 100 residential and commercial buildings across Rwanda and has expertise in sustainable construction practices.',
                'short_bio': 'Senior Structural Engineer specializing in building design and seismic analysis',
                'qualifications': 'BSc Structural Engineering, MSc Earthquake Engineering, LEED AP',
                'experience_years': 12,
                'specializations': ['Structural Design', 'Seismic Analysis', 'Sustainable Construction', 'Building Codes'],
                'email': 'marie@nupoconsult.rw',
                'linkedin_url': 'https://linkedin.com/in/marie-mukamana'
            },
            {
                'name': 'David NKURUNZIZA',
                'position': 'Project Manager & Construction Supervisor',
                'position_type': 'manager',
                'bio': 'David brings 10 years of project management experience with a track record of delivering complex construction projects on time and within budget. He specializes in construction supervision, quality control, and stakeholder management.',
                'short_bio': 'Experienced Project Manager with expertise in construction supervision and quality control',
                'qualifications': 'BSc Construction Management, PMP Certification, OSHA Safety Certification',
                'experience_years': 10,
                'specializations': ['Project Management', 'Construction Supervision', 'Quality Control', 'Safety Management'],
                'email': 'david@nupoconsult.rw',
                'linkedin_url': 'https://linkedin.com/in/david-nkurunziza'
            },
            {
                'name': 'Dr. Grace UWIMANA',
                'position': 'Environmental Engineer & Sustainability Specialist',
                'position_type': 'specialist',
                'bio': 'Dr. Grace is an environmental engineer with a PhD in Environmental Science and 8 years of experience in environmental impact assessments and sustainable engineering solutions. She has worked on major infrastructure projects across the region.',
                'short_bio': 'Environmental Engineer and Sustainability Specialist with PhD in Environmental Science',
                'qualifications': 'PhD Environmental Science, MSc Environmental Engineering, EIA Certified Professional',
                'experience_years': 8,
                'specializations': ['Environmental Impact Assessment', 'Sustainability', 'Water Treatment', 'Waste Management'],
                'email': 'grace@nupoconsult.rw',
                'linkedin_url': 'https://linkedin.com/in/grace-uwimana'
            },
            {
                'name': 'Eng. Patrick HABIMANA',
                'position': 'Transportation Engineer',
                'position_type': 'engineer',
                'bio': 'Patrick specializes in transportation engineering with 9 years of experience in road design, traffic analysis, and transportation planning. He has been involved in several major highway projects in Rwanda.',
                'short_bio': 'Transportation Engineer specializing in road design and traffic analysis',
                'qualifications': 'MSc Transportation Engineering, Traffic Engineering Certification',
                'experience_years': 9,
                'specializations': ['Road Design', 'Traffic Analysis', 'Transportation Planning', 'Highway Engineering'],
                'email': 'patrick@nupoconsult.rw'
            },
            {
                'name': 'Alice NYIRAHABIMANA',
                'position': 'Water Resources Engineer',
                'position_type': 'engineer',
                'bio': 'Alice is a water resources engineer with 7 years of experience in water supply systems, irrigation, and hydraulic design. She has designed water systems serving over 50,000 people across rural Rwanda.',
                'short_bio': 'Water Resources Engineer with expertise in water supply systems and hydraulic design',
                'qualifications': 'BSc Water Resources Engineering, Hydraulic Design Certification',
                'experience_years': 7,
                'specializations': ['Water Supply Systems', 'Irrigation Design', 'Hydraulic Analysis', 'Pump Systems'],
                'email': 'alice@nupoconsult.rw'
            }
        ]
        
        for member_data in team_data:
            member, created = TeamMember.objects.get_or_create(
                name=member_data['name'],
                defaults={
                    'slug': slugify(member_data['name']),
                    'position': member_data['position'],
                    'position_type': member_data['position_type'],
                    'bio': member_data['bio'],
                    'short_bio': member_data['short_bio'],
                    'qualifications': member_data['qualifications'],
                    'experience_years': member_data['experience_years'],
                    'specializations': member_data['specializations'],
                    'email': member_data.get('email', ''),
                    'linkedin_url': member_data.get('linkedin_url', ''),
                    'is_active': True,
                    'is_featured': member_data['position_type'] in ['ceo', 'manager', 'engineer'],
                    'order': random.randint(1, 10)
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created team member: {member_data["name"]}')

    def create_partners(self):
        partners_data = [
            {
                'name': 'Ministry of Infrastructure (MININFRA)',
                'partner_type': 'government',
                'description': 'Strategic partnership with Rwanda\'s Ministry of Infrastructure for national development projects'
            },
            {
                'name': 'Rwanda Development Board (RDB)',
                'partner_type': 'government',
                'description': 'Collaboration on investment promotion and infrastructure development initiatives'
            },
            {
                'name': 'University of Rwanda - College of Science and Technology',
                'partner_type': 'academic',
                'description': 'Academic partnership for research and development in engineering solutions'
            },
            {
                'name': 'East African Development Bank',
                'partner_type': 'international',
                'description': 'Financial partnership for major infrastructure development projects'
            },
            {
                'name': 'Kigali City Council',
                'partner_type': 'government',
                'description': 'Municipal partnership for urban development and infrastructure projects'
            },
            {
                'name': 'Private Sector Federation Rwanda',
                'partner_type': 'private',
                'description': 'Industry collaboration for private sector infrastructure development'
            },
            {
                'name': 'Engineers Without Borders Rwanda',
                'partner_type': 'ngo',
                'description': 'NGO partnership for community development and capacity building projects'
            },
            {
                'name': 'African Development Bank',
                'partner_type': 'international',
                'description': 'International development partnership for large-scale infrastructure projects'
            }
        ]
        
        for partner_data in partners_data:
            partner, created = Partner.objects.get_or_create(
                name=partner_data['name'],
                defaults={
                    'slug': slugify(partner_data['name']),
                    'partner_type': partner_data['partner_type'],
                    'description': partner_data['description'],
                    'partnership_start_date': timezone.now().date() - timedelta(days=random.randint(365, 1825)),
                    'is_active': True,
                    'is_featured': random.choice([True, False]),
                    'order': random.randint(1, 10)
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created partner: {partner_data["name"]}')

    def create_news_articles(self):
        # Create a sample user for articles
        author, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@nupoconsult.rw',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            author.set_password('admin123')
            author.save()
            self.stdout.write('  ✓ Created admin user (username: admin, password: admin123)')

        articles_data = [
            {
                'title': 'NUPO Consult Wins Major Infrastructure Contract',
                'article_type': 'news',
                'excerpt': 'We are proud to announce that NUPO Consult has been awarded a major infrastructure development contract worth $2.5 million.',
                'content': '''We are excited to announce that NUPO Consult Ltd has been awarded a significant infrastructure development contract by the Ministry of Infrastructure. This $2.5 million project involves the design and supervision of a 15-kilometer rural road network in the Eastern Province.

The project will connect three rural communities to the main highway, improving access to markets, schools, and healthcare facilities for over 10,000 residents. Our team will be responsible for the complete engineering design, environmental impact assessment, and construction supervision.

"This project aligns perfectly with our mission to contribute to Rwanda's sustainable development," said Jean Baptiste Uwimana, CEO of NUPO Consult. "We are committed to delivering high-quality infrastructure that will have a lasting positive impact on these communities."

The project is expected to commence in the next quarter and will be completed within 18 months. This contract further establishes NUPO Consult as a leading engineering consultancy in Rwanda's infrastructure development sector.'''
            },
            {
                'title': 'Sustainable Building Design: Our Commitment to Green Engineering',
                'article_type': 'sustainability',
                'excerpt': 'Learn about our innovative approaches to sustainable building design and how we\'re contributing to Rwanda\'s green building movement.',
                'content': '''At NUPO Consult, we believe that sustainable engineering is not just an option—it's a responsibility. As Rwanda continues to develop rapidly, we are committed to ensuring that growth happens in harmony with environmental conservation.

Our sustainable building design approach incorporates several key principles:

**Energy Efficiency**: We design buildings that minimize energy consumption through optimal orientation, natural lighting, and efficient HVAC systems.

**Local Materials**: We prioritize the use of locally sourced, sustainable materials that reduce transportation costs and support local economies.

**Water Conservation**: Our designs include rainwater harvesting systems, greywater recycling, and efficient plumbing fixtures.

**Waste Reduction**: We implement construction waste management plans and design for building longevity and adaptability.

Recent projects have achieved up to 40% reduction in energy consumption compared to conventional designs. We are also working towards LEED certification for several of our commercial projects.

"Sustainable design is not just about environmental protection—it's about creating buildings that are economically viable and socially beneficial," explains Dr. Grace Uwimana, our Environmental Engineer.

We invite other engineering firms and developers to join us in this commitment to sustainable development.'''
            },
            {
                'title': 'Team Achievement: Marie Mukamana Receives Professional Excellence Award',
                'article_type': 'award',
                'excerpt': 'We congratulate our Senior Structural Engineer Marie Mukamana on receiving the Rwanda Engineers Board Professional Excellence Award.',
                'content': '''We are delighted to announce that our Senior Structural Engineer, Marie Mukamana, has been honored with the Rwanda Engineers Board Professional Excellence Award for 2023.

This prestigious award recognizes Marie's outstanding contributions to structural engineering in Rwanda, particularly her innovative work in seismic-resistant building design and her commitment to mentoring young engineers.

Over the past year, Marie has:

- Led the structural design of 15 major building projects
- Developed new seismic analysis protocols for high-rise buildings
- Mentored 8 junior engineers through the Rwanda Engineers Board program
- Published 3 technical papers on earthquake-resistant construction

"Marie's dedication to excellence and innovation exemplifies the values we hold dear at NUPO Consult," said CEO Jean Baptiste Uwimana. "Her work not only advances our company but contributes significantly to the engineering profession in Rwanda."

The award ceremony was held at the Kigali Convention Centre, attended by over 200 engineering professionals from across East Africa.

Marie will represent Rwanda at the upcoming African Engineering Excellence Conference in Nairobi, where she will present her research on cost-effective seismic design solutions for developing countries.

Congratulations, Marie! We are proud to have you as part of our team.'''
            },
            {
                'title': 'New Water Treatment Plant Project Launched in Musanze',
                'article_type': 'project',
                'excerpt': 'NUPO Consult begins work on a new water treatment facility that will serve 25,000 residents in Musanze District.',
                'content': '''NUPO Consult has officially launched the design and construction supervision of a new water treatment plant in Musanze District, Northern Province. This facility will provide clean, safe drinking water to approximately 25,000 residents across 12 villages.

**Project Overview:**

- Treatment capacity: 2,500 cubic meters per day
- Service area: 12 villages in Musanze District
- Beneficiaries: 25,000 residents
- Project duration: 14 months
- Total investment: $1.8 million

The project is funded by the African Development Bank in partnership with the Government of Rwanda and represents a significant step toward achieving universal access to clean water in rural areas.

**Technical Features:**

- Advanced filtration systems
- Solar-powered pumping stations
- Remote monitoring capabilities
- Backup power systems
- Water quality testing laboratory

Our team, led by Water Resources Engineer Alice Nyirahabimana, will oversee all aspects of the project from detailed design through commissioning and staff training.

"Access to clean water is fundamental to community health and development," said Alice. "This project will not only provide safe drinking water but also support local economic activities and improve quality of life."

The project includes comprehensive community engagement and training programs to ensure sustainable operation and maintenance of the facility.

Construction is expected to begin in the next two months, with the facility becoming operational by the end of next year.'''
            },
            {
                'title': 'Industry Insights: The Future of Transportation Engineering in Rwanda',
                'article_type': 'industry',
                'excerpt': 'Our Transportation Engineer Patrick Habimana shares insights on emerging trends and technologies shaping Rwanda\'s transportation infrastructure.',
                'content': '''As Rwanda continues its rapid economic development, the transportation sector is experiencing unprecedented growth and transformation. Our Transportation Engineer, Patrick Habimana, shares his insights on the key trends shaping the future of transportation engineering in Rwanda.

**Smart Transportation Systems**

The integration of intelligent transportation systems (ITS) is revolutionizing how we design and manage road networks. GPS-based traffic management, smart traffic signals, and real-time monitoring systems are becoming standard features in new projects.

**Sustainable Transportation**

There's a growing emphasis on sustainable transportation solutions, including:

- Electric vehicle charging infrastructure
- Bicycle and pedestrian-friendly road designs
- Public transportation optimization
- Green construction materials for road projects

**Regional Connectivity**

Rwanda's strategic location as a gateway to East and Central Africa is driving investment in regional transportation corridors. The Northern Corridor and Central Corridor projects are creating new opportunities for transportation engineers.

**Technology Integration**

Modern transportation projects increasingly incorporate:

- GIS mapping and analysis
- 3D modeling and visualization
- Drone surveys and monitoring
- Mobile-based project management

**Challenges and Opportunities**

Key challenges include:

- Balancing rapid development with environmental protection
- Ensuring rural connectivity while focusing on urban growth
- Managing increasing traffic volumes in urban areas
- Building climate-resilient infrastructure

"The next decade will see transportation engineering in Rwanda evolve from traditional road building to comprehensive mobility solutions," explains Patrick. "We're not just building roads—we're creating integrated transportation ecosystems."

**Looking Ahead**

NUPO Consult is investing in new technologies and training to stay at the forefront of these developments. We're particularly excited about opportunities in:

- Smart city transportation planning
- Sustainable urban mobility
- Regional trade corridor development
- Climate-adaptive infrastructure design

The future of transportation engineering in Rwanda is bright, and we're proud to be part of this transformation.'''
            }
        ]
        
        for article_data in articles_data:
            article, created = NewsArticle.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'slug': slugify(article_data['title']),
                    'article_type': article_data['article_type'],
                    'excerpt': article_data['excerpt'],
                    'content': article_data['content'],
                    'author': author,
                    'is_published': True,
                    'is_featured': random.choice([True, False]),
                    'published_date': timezone.now() - timedelta(days=random.randint(1, 90)),
                    'views_count': random.randint(50, 500)
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created article: {article_data["title"]}')

    def create_projects(self):
        # Get some services and team members for project relationships
        services = list(Service.objects.all())
        team_members = list(TeamMember.objects.all())
        
        projects_data = [
            {
                'name': 'Kigali-Musanze Highway Upgrade',
                'client': 'Ministry of Infrastructure',
                'project_type': 'infrastructure',
                'status': 'completed',
                'description': 'Complete upgrade of the 85-kilometer highway connecting Kigali to Musanze, including road widening, bridge construction, and drainage improvements.',
                'location': 'Kigali to Musanze, Northern Province',
                'start_date': timezone.now().date() - timedelta(days=730),
                'end_date': timezone.now().date() - timedelta(days=90),
                'budget': 45000000.00
            },
            {
                'name': 'Green Hills Residential Complex',
                'client': 'Green Hills Development Ltd',
                'project_type': 'residential',
                'status': 'construction',
                'description': 'Design and construction supervision of a 120-unit residential complex featuring sustainable design elements and modern amenities.',
                'location': 'Nyarutarama, Kigali',
                'start_date': timezone.now().date() - timedelta(days=180),
                'end_date': None,
                'budget': 8500000.00
            },
            {
                'name': 'Kigali Convention Centre Expansion',
                'client': 'Rwanda Development Board',
                'project_type': 'commercial',
                'status': 'design',
                'description': 'Structural design for the expansion of Kigali Convention Centre including a new exhibition hall and conference facilities.',
                'location': 'Kimihurura, Kigali',
                'start_date': timezone.now().date() - timedelta(days=60),
                'end_date': None,
                'budget': 12000000.00
            },
            {
                'name': 'Rural Water Supply Network - Eastern Province',
                'client': 'Water and Sanitation Corporation (WASAC)',
                'project_type': 'infrastructure',
                'status': 'completed',
                'description': 'Design and supervision of water supply network serving 15 rural communities with treatment plants, distribution systems, and storage facilities.',
                'location': 'Rwamagana District, Eastern Province',
                'start_date': timezone.now().date() - timedelta(days=540),
                'end_date': timezone.now().date() - timedelta(days=30),
                'budget': 3200000.00
            },
            {
                'name': 'University of Rwanda Engineering Building',
                'client': 'University of Rwanda',
                'project_type': 'institutional',
                'status': 'completed',
                'description': 'Complete structural and MEP design for a new 5-story engineering faculty building with laboratories and lecture halls.',
                'location': 'Huye, Southern Province',
                'start_date': timezone.now().date() - timedelta(days=450),
                'end_date': timezone.now().date() - timedelta(days=120),
                'budget': 6800000.00
            },
            {
                'name': 'Nyabugogo Industrial Park Infrastructure',
                'client': 'Rwanda Development Board',
                'project_type': 'industrial',
                'status': 'construction',
                'description': 'Infrastructure development for industrial park including roads, utilities, drainage systems, and waste treatment facilities.',
                'location': 'Nyabugogo, Kigali',
                'start_date': timezone.now().date() - timedelta(days=120),
                'end_date': None,
                'budget': 15000000.00
            },
            {
                'name': 'Butare-Cyangugu Road Rehabilitation',
                'client': 'Rwanda Transport Development Agency',
                'project_type': 'infrastructure',
                'status': 'planning',
                'description': 'Rehabilitation and upgrading of 95-kilometer road connecting Butare to Cyangugu with improved drainage and safety features.',
                'location': 'Southern Province',
                'start_date': timezone.now().date() + timedelta(days=30),
                'end_date': None,
                'budget': 28000000.00
            },
            {
                'name': 'Kigali Heights Shopping Mall',
                'client': 'Kigali Heights Development',
                'project_type': 'commercial',
                'status': 'design',
                'description': 'Structural design and MEP systems for a modern 4-level shopping mall with parking facilities and entertainment areas.',
                'location': 'Remera, Kigali',
                'start_date': timezone.now().date() - timedelta(days=45),
                'end_date': None,
                'budget': 9500000.00
            }
        ]
        
        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                name=project_data['name'],
                defaults={
                    'slug': slugify(project_data['name']),
                    'client': project_data['client'],
                    'project_type': project_data['project_type'],
                    'status': project_data['status'],
                    'description': project_data['description'],
                    'location': project_data['location'],
                    'start_date': project_data['start_date'],
                    'end_date': project_data['end_date'],
                    'budget': project_data['budget'],
                    'is_featured': random.choice([True, False]),
                    'is_public': True
                }
            )
            
            if created:
                # Add random services and team members
                if services:
                    project_services = random.sample(services, min(3, len(services)))
                    project.services_provided.set(project_services)
                
                if team_members:
                    project_team = random.sample(team_members, min(4, len(team_members)))
                    project.team_members.set(project_team)
                
                self.stdout.write(f'  ✓ Created project: {project_data["name"]}')

    def create_testimonials(self):
        projects = list(Project.objects.all())
        services = list(Service.objects.all())
        
        testimonials_data = [
            {
                'client_name': 'Dr. James Gasana',
                'client_company': 'Ministry of Infrastructure',
                'client_position': 'Director of Infrastructure Development',
                'content': 'NUPO Consult delivered exceptional results on our highway upgrade project. Their technical expertise, attention to detail, and commitment to deadlines made them an invaluable partner. The project was completed on time and within budget.',
                'rating': 5
            },
            {
                'client_name': 'Sarah Uwimana',
                'client_company': 'Green Hills Development Ltd',
                'client_position': 'Project Manager',
                'content': 'Working with NUPO Consult on our residential complex has been a pleasure. Their innovative design solutions and sustainable approach aligned perfectly with our vision. The team\'s professionalism and expertise are outstanding.',
                'rating': 5
            },
            {
                'client_name': 'Prof. Emmanuel Ntaganda',
                'client_company': 'University of Rwanda',
                'client_position': 'Dean of Engineering',
                'content': 'The engineering building designed by NUPO Consult has exceeded our expectations. The functionality, aesthetics, and sustainability features make it a model for modern educational facilities. Highly recommended.',
                'rating': 5
            },
            {
                'client_name': 'Marie Claire Mukamana',
                'client_company': 'WASAC Ltd',
                'client_position': 'Regional Manager',
                'content': 'NUPO Consult\'s water supply project has transformed our rural communities. Their comprehensive approach, from design to community training, ensures long-term sustainability. Excellent work!',
                'rating': 5
            },
            {
                'client_name': 'John Habimana',
                'client_company': 'Kigali Heights Development',
                'client_position': 'CEO',
                'content': 'The structural design expertise provided by NUPO Consult for our shopping mall project is top-notch. Their innovative solutions helped us optimize space while ensuring safety and compliance with all regulations.',
                'rating': 4
            },
            {
                'client_name': 'Agnes Nyiramana',
                'client_company': 'Private Homeowner',
                'client_position': 'Homeowner',
                'content': 'NUPO Consult designed our family home with great attention to our needs and budget. The result is a beautiful, functional, and energy-efficient home. We couldn\'t be happier with their service.',
                'rating': 5
            }
        ]
        
        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                client_name=testimonial_data['client_name'],
                defaults={
                    'client_company': testimonial_data['client_company'],
                    'client_position': testimonial_data['client_position'],
                    'content': testimonial_data['content'],
                    'rating': testimonial_data['rating'],
                    'project': random.choice(projects) if projects else None,
                    'service': random.choice(services) if services else None,
                    'is_approved': True,
                    'is_featured': random.choice([True, False])
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created testimonial: {testimonial_data["client_name"]}')

    def create_sample_inquiries(self):
        services = list(Service.objects.all())
        
        inquiries_data = [
            {
                'name': 'Peter Nkurunziza',
                'email': 'peter.nkurunziza@email.com',
                'phone': '+250 788 111 222',
                'company': 'Nkurunziza Construction Ltd',
                'inquiry_type': 'quote',
                'subject': 'Structural Design for Office Building',
                'message': 'We need structural design services for a 3-story office building in Kimisagara. The building will have commercial space on the ground floor and offices on upper floors. Please provide a quote.',
                'project_budget': '50k-100k',
                'project_timeline': '3-6-months',
                'priority': 'medium'
            },
            {
                'name': 'Alice Mukamana',
                'email': 'alice.mukamana@gmail.com',
                'phone': '+250 788 333 444',
                'company': '',
                'inquiry_type': 'consultation',
                'subject': 'Home Extension Design',
                'message': 'I would like to extend my house by adding two bedrooms and a bathroom. I need consultation on the feasibility and design options.',
                'project_budget': '10k-50k',
                'project_timeline': '1-3-months',
                'priority': 'low'
            },
            {
                'name': 'Emmanuel Habimana',
                'email': 'e.habimana@cooperatives.gov.rw',
                'phone': '+250 788 555 666',
                'company': 'Ministry of Trade and Industry',
                'inquiry_type': 'general',
                'subject': 'Industrial Park Infrastructure Development',
                'message': 'We are planning to develop a new industrial park and need comprehensive engineering services including site planning, utilities design, and environmental assessment.',
                'project_budget': 'over-500k',
                'project_timeline': '6-12-months',
                'priority': 'high'
            }
        ]
        
        for inquiry_data in inquiries_data:
            inquiry, created = ContactInquiry.objects.get_or_create(
                email=inquiry_data['email'],
                defaults={
                    'name': inquiry_data['name'],
                    'phone': inquiry_data['phone'],
                    'company': inquiry_data['company'],
                    'inquiry_type': inquiry_data['inquiry_type'],
                    'subject': inquiry_data['subject'],
                    'message': inquiry_data['message'],
                    'project_budget': inquiry_data['project_budget'],
                    'project_timeline': inquiry_data['project_timeline'],
                    'priority': inquiry_data['priority'],
                    'is_responded': random.choice([True, False])
                }
            )
            
            if created and services:
                # Add random services
                interested_services = random.sample(services, min(2, len(services)))
                inquiry.services_interested.set(interested_services)
                
                self.stdout.write(f'  ✓ Created inquiry: {inquiry_data["name"]}')

    def create_newsletter_subscribers(self):
        subscribers_data = [
            {'email': 'john.doe@email.com', 'name': 'John Doe'},
            {'email': 'jane.smith@gmail.com', 'name': 'Jane Smith'},
            {'email': 'engineer@company.rw', 'name': 'Engineering Professional'},
            {'email': 'student@ur.ac.rw', 'name': 'Engineering Student'},
            {'email': 'contractor@construction.rw', 'name': 'Construction Contractor'},
            {'email': 'architect@design.com', 'name': 'Architect'},
            {'email': 'developer@property.rw', 'name': 'Property Developer'},
            {'email': 'consultant@advisory.com', 'name': 'Engineering Consultant'},
        ]
        
        for subscriber_data in subscribers_data:
            subscriber, created = Newsletter.objects.get_or_create(
                email=subscriber_data['email'],
                defaults={
                    'name': subscriber_data['name'],
                    'is_active': True,
                    'subscribed_date': timezone.now() - timedelta(days=random.randint(1, 365))
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created subscriber: {subscriber_data["email"]}')

    def create_seo_settings(self):
        seo_pages = [
            {
                'page_name': 'home',
                'meta_title': 'NUPO Consult Ltd - Rwanda\'s Leading Engineering Partner',
                'meta_description': 'Leading engineering consultancy in Rwanda providing comprehensive engineering solutions for infrastructure, construction, and development projects. Expert team, proven results.',
                'meta_keywords': 'engineering consultancy Rwanda, infrastructure development, construction management, structural engineering, civil engineering, project management, Kigali engineers'
            },
            {
                'page_name': 'services',
                'meta_title': 'Engineering Services - NUPO Consult Ltd',
                'meta_description': 'Comprehensive engineering services including structural design, civil engineering, project management, environmental engineering, and consulting services in Rwanda.',
                'meta_keywords': 'engineering services Rwanda, structural design, civil engineering, project management, environmental engineering, construction supervision'
            },
            {
                'page_name': 'projects',
                'meta_title': 'Our Projects - NUPO Consult Ltd Portfolio',
                'meta_description': 'Explore our portfolio of successful engineering projects including infrastructure development, building construction, and water systems across Rwanda.',
                'meta_keywords': 'engineering projects Rwanda, infrastructure projects, construction projects, building design, road construction, water systems'
            },
            {
                'page_name': 'about',
                'meta_title': 'About NUPO Consult Ltd - Rwanda Engineering Experts',
                'meta_description': 'Learn about NUPO Consult Ltd, Rwanda\'s trusted engineering consultancy firm. Our mission, vision, values, and expert team committed to excellence.',
                'meta_keywords': 'about NUPO Consult, engineering company Rwanda, engineering consultancy, professional engineers Rwanda, company history'
            },
            {
                'page_name': 'contact',
                'meta_title': 'Contact NUPO Consult Ltd - Get Engineering Quote',
                'meta_description': 'Contact NUPO Consult Ltd for professional engineering services. Get a free consultation and quote for your construction or infrastructure project.',
                'meta_keywords': 'contact engineers Rwanda, engineering consultation, project quote, engineering services inquiry, NUPO Consult contact'
            },
            {
                'page_name': 'team',
                'meta_title': 'Our Expert Team - NUPO Consult Ltd Engineers',
                'meta_description': 'Meet our team of experienced professional engineers, project managers, and specialists at NUPO Consult Ltd. Expertise you can trust.',
                'meta_keywords': 'engineering team Rwanda, professional engineers, project managers, engineering specialists, NUPO Consult staff'
            },
            {
                'page_name': 'news',
                'meta_title': 'News & Updates - NUPO Consult Ltd',
                'meta_description': 'Stay updated with the latest news, project updates, industry insights, and achievements from NUPO Consult Ltd, Rwanda\'s leading engineering firm.',
                'meta_keywords': 'engineering news Rwanda, project updates, industry insights, engineering achievements, NUPO Consult news'
            }
        ]
        
        for seo_data in seo_pages:
            seo, created = SEOSettings.objects.get_or_create(
                page_name=seo_data['page_name'],
                defaults={
                    'meta_title': seo_data['meta_title'],
                    'meta_description': seo_data['meta_description'],
                    'meta_keywords': seo_data['meta_keywords'],
                    'robots_meta': 'index, follow'
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created SEO settings: {seo_data["page_name"]}')
