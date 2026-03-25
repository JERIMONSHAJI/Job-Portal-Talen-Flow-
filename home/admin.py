from django.contrib import admin
from .models import userprofile,companyprofile,jobtypes,skills,job,workmode,application

admin.site.register(userprofile)
admin.site.register(jobtypes)
admin.site.register(job)
admin.site.register(companyprofile)
admin.site.register(skills)
admin.site.register(workmode)
admin.site.register(application)