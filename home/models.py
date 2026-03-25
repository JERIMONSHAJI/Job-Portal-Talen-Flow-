from django.db import models
from django.contrib.auth.models import User

class skills(models.Model):
    name=models.TextField(max_length=15)

    def __str__(self):
        return self.name
    
class userprofile(models.Model):
    image=models.ImageField(upload_to='profile')
    phone=models.IntegerField()
    email=models.EmailField(null=True,blank=True)
    about=models.TextField(max_length=200,null=True,blank=True)
    location=models.TextField(max_length=15)
    user_skills = models.ManyToManyField(skills, blank=True)
    us=models.OneToOneField(User,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return str(self.us)

class companyprofile(models.Model):
    image=models.ImageField(upload_to='companyprofile')
    email=models.EmailField()
    tagline=models.TextField(max_length=100,blank=True,null=True)
    about=models.TextField(max_length=500,blank=True,null=True)
    location=models.TextField(max_length=15)
    us=models.OneToOneField(User,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return str(self.us)
    
class jobtypes(models.Model):
    name=models.TextField(max_length=15)

    def __str__(self):
        return self.name
    
class workmode(models.Model):
    name=models.TextField(max_length=15)

    def __str__(self):
        return self.name
    
class job(models.Model):
    name=models.TextField(max_length=20)
    company=models.ForeignKey(companyprofile,on_delete=models.CASCADE,default=1)
    description=models.TextField(max_length=200)
    salary=models.TextField(max_length=20)
    jobtype=models.ForeignKey(jobtypes,on_delete=models.CASCADE, null=True, blank=True)
    workmd=models.ForeignKey(workmode,on_delete=models.CASCADE,null=True,blank=True)
    experience=models.TextField(max_length=15,null=True,blank=True)
    required_skills=models.ManyToManyField(skills,blank=True)
    posted_at   = models.DateTimeField(auto_now_add=True)
    expires_at  = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_job = models.ForeignKey(job, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='Pending'
    )

    class Meta:
        unique_together = ('applicant', 'applied_job')

    def __str__(self):
        return f"{self.applicant} - {self.applied_job} ({self.status})"

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
    
    return render(request, 'profile_detail.html', context)