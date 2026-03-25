from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from home.models import job,companyprofile,userprofile,application,skills
from .forms import JobEditForm,JobForm,UserProfileForm, CompanyProfileForm
from django.db.models import Q, IntegerField, Value
from django.db.models.functions import Cast, Replace, Trim
from django.core.paginator import Paginator

def loginfn(request):
    if request.method == 'POST':
        u = request.POST['un']
        p = request.POST['ps1']
        user = auth.authenticate(username=u, password=p)

        if user:
            auth.login(request, user)

            if hasattr(user, 'userprofile'):
                if user.userprofile.phone == 0:
                    return redirect('/editprofile')
            
            elif hasattr(user, 'companyprofile'):
                if user.companyprofile.image == "":
                    return redirect('/editprofile')

            return redirect('/')
        else:
            return render(request, 'login.html', {'er': 'User Not Found or invalid password'})
    return render(request, 'login.html')

def registerfn(request):
    if request.method == "POST":
        user_type = request.POST.get('userType')
        password = request.POST.get('password')
        confirm_password = request.POST.get('cpassword')
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'register.html') 

        if user_type == "employee":
            username = request.POST.get('username')
            full_name = request.POST.get('full_name')
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
                return render(request, 'register.html') 
            
            user = User.objects.create_user(username=username, password=password)
            user.first_name = full_name
            user.save()
            userprofile.objects.create(us=user, phone=0, location="Unknown")

        elif user_type == "company":
            company_name = request.POST.get('company_name')
            location = request.POST.get('location')
            username = company_name.replace(" ", "_").lower()
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
                return render(request, 'register.html') 

            user = User.objects.create_user(username=username, password=password)
            companyprofile.objects.create(us=user, location=location, email=f"info@{username}.com")
        messages.success(request, "Registration successful! Please login.")
        return redirect('/login')

    return render(request, 'register.html')

@login_required(login_url='/login/')
def homefn(request) :
    randjobs=job.objects.order_by('posted_at')[:3]
    return render(request,'home.html',{'jobs':randjobs})

@login_required(login_url='/login/')
def findjobfn(request):
    query = request.GET.get('q')
    min_salary = request.GET.get('min_salary')
    selected_job_types = request.GET.getlist('job_type') 
    selected_work_modes = request.GET.getlist('work_mode')
    
    if query:
        randjobs = job.objects.filter(
            Q(name__icontains=query) | 
            Q(company__us__username__icontains=query) | 
            Q(description__icontains=query)
        ).distinct()
    else:
        randjobs = job.objects.all().order_by('-posted_at')

    if min_salary and min_salary.isdigit():
        randjobs = randjobs.annotate(
            salary_num=Cast(
                Trim(Replace(Replace('salary', Value('LPA'), Value('')), Value(','), Value(''))),
                output_field=IntegerField()
            )
        ).filter(salary_num__gte=int(min_salary))

    if selected_job_types:
        randjobs = randjobs.filter(jobtype__name__in=selected_job_types)

    if selected_work_modes:
        randjobs = randjobs.filter(workmd__name__in=selected_work_modes)

    paginator = Paginator(randjobs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'jobs': page_obj,
        'query': query,
        'min_salary': min_salary,
        'selected_types': selected_job_types,
        'selected_modes': selected_work_modes
    }
    return render(request, 'findjob.html', context)

@login_required(login_url='/login/')
def viewfn(request,pid):
    j=job.objects.get(id=pid)
    return render(request,'view.html',{'jobs':j})

@login_required(login_url='/login/')
def profilefn(request):
    user_data = None
    company_data = None
    role = None

    try:
        user_data = request.user.userprofile
        role = 'user'
    except userprofile.DoesNotExist:
        try:
            company_data = request.user.companyprofile
            role = 'company'
        except companyprofile.DoesNotExist:
            role = 'none'

    context = {
        'user_data': user_data,
        'company_data': company_data,
        'role': role
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/login/')
def dashboardfn(request):
    jobs_to_display = []
    user_type = None

    if hasattr(request.user, 'companyprofile'):
        user_type = 'company'
        jobs_to_display = job.objects.filter(company=request.user.companyprofile)
        
    elif hasattr(request.user, 'userprofile'):
        user_type = 'user'
        jobs_to_display = application.objects.filter(applicant=request.user)

    context = {
        'jobs': jobs_to_display,
        'user_type': user_type
    }
    return render(request, 'dashboard.html', context)

def logoutfn(request) :
    auth.logout(request)
    return redirect("/login")

def applayfn(request, jid):
    uprofile = request.user
    tjob = job.objects.get(id=jid)
    
    already_applied = application.objects.filter(applicant=uprofile, applied_job=tjob).exists()
    
    if already_applied:
        messages.warning(request, f"You have already applied for the {tjob.name} position.")
    else:
        app = application(applicant=uprofile, applied_job=tjob)
        app.save()
        messages.success(request, f"Successfully applied for {tjob.name}!")
        
    return redirect("/findjob/")

def editfn(request, jid):
    job_instance = job.objects.get(id=jid)

    if request.method == 'POST':
        form = JobEditForm(request.POST, instance=job_instance)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/') 
    else:
        existing_skills = ", ".join([s.name for s in job_instance.required_skills.all()])
        form = JobEditForm(instance=job_instance, initial={'custom_skills': existing_skills})

    return render(request, 'edit.html', {'form': form, 'job': job_instance})

@login_required
def editprofilefn(request):
    user_prof = userprofile.objects.filter(us=request.user).first()
    comp_prof = companyprofile.objects.filter(us=request.user).first()

    if user_prof:
        form = UserProfileForm(request.POST or None, request.FILES or None, instance=user_prof)
        template_name = 'edit_user_profile.html'
    elif comp_prof:
        form = CompanyProfileForm(request.POST or None, request.FILES or None, instance=comp_prof)
        template_name = 'editcompanyprofile.html'
    else:
        return redirect('/profile')
    
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            if user_prof:
                new_skills_raw = form.cleaned_data.get('add_new_skills')
                
                if new_skills_raw:
                    skill_names = [s.strip() for s in new_skills_raw.split(',') if s.strip()]
                    
                    for name in skill_names:
                        skill_obj, created = skills.objects.get_or_create(name=name)
                        instance.user_skills.add(skill_obj)
            
            return redirect('/profile')
    return render(request, template_name, {'form': form})

@login_required
def addjobfn(request):
    try:
        current_company = companyprofile.objects.get(us=request.user)
    except companyprofile.DoesNotExist:
        return redirect('dashboard')

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            new_job = form.save(commit=False)
            new_job.company = current_company
            
            new_job.save()
            
            skills_str = form.cleaned_data.get('custom_skills')
            if skills_str:
                skill_list = [s.strip() for s in skills_str.split(',') if s.strip()]
                for name in skill_list:
                    skill_obj, created = skills.objects.get_or_create(name=name)
                    new_job.required_skills.add(skill_obj)
            
            return redirect('/dashboard/')
    else:
        form = JobForm()
        
    return render(request, 'addjob.html', {'form': form})

def deletefn(request, jid) :
    x=job.objects.get(id=jid)
    x.delete()
    return redirect('/dashboard/')

@login_required
def viewapplicantsfn(request, jid):
    current_company = get_object_or_404(companyprofile, us=request.user)
    target_job = get_object_or_404(job, id=jid, company=current_company)
    applicants = application.objects.filter(applied_job=target_job).order_by('applied_at')
    
    context = {
        'target_job': target_job,
        'applicants': applicants,
    }
    return render(request, 'viewapplicants.html', context)

@login_required
def update_status_fn(request, aid, status):
    app = get_object_or_404(application, id=aid)
    if app.applied_job.company.us == request.user:
        app.status = status
        app.save()
        messages.success(request, f"Status for {app.applicant.username} successfully updated to {status}.")
    else:
        messages.error(request, "You do not have permission to perform this action.")
    return redirect(f'/applicants/{app.applied_job.id}/')

def profile_view(request, pk):
    target_user = User.objects.filter(pk=pk).first()
    
    profile = None
    user_type = None

    if target_user:
        if hasattr(target_user, 'userprofile'):
            profile = target_user.userprofile
            user_type = 'seeker'
        elif hasattr(target_user, 'companyprofile'):
            profile = target_user.companyprofile
            user_type = 'company'

    context = {
        'viewed_user': target_user,
        'profile': profile,
        'user_type': user_type,
    }
    
    return render(request, 'visitprofile.html', context)

def contactusfn(request) :
    return render(request, 'contactus.html')