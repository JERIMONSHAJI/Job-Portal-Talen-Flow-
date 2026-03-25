from django import forms
from .models import job, skills,userprofile,companyprofile

class JobEditForm(forms.ModelForm):
    custom_skills = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Django, AWS'}),
        help_text="Separate skills with commas"
    )

    class Meta:
        model = job
        fields = ['name', 'salary', 'jobtype', 'workmd', 'experience', 'description', 'expires_at']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.TextInput(attrs={'class': 'form-control'}),
            'jobtype': forms.Select(attrs={'class': 'form-select'}),
            'workmd': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'expires_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        
        skills_str = self.cleaned_data.get('custom_skills')
        if skills_str:
            skill_list = [s.strip() for s in skills_str.split(',') if s.strip()]
            for skill_name in skill_list:
                skill_obj, created = skills.objects.get_or_create(name=skill_name)
                instance.required_skills.add(skill_obj)
        
        return instance
    
class UserProfileForm(forms.ModelForm):
    add_new_skills = forms.CharField(
        max_length=100, 
        required=False, 
        label="Add skills not listed",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Docker, Figma (comma separated)'})
    )

    class Meta:
        model = userprofile
        fields = ['image', 'phone', 'email', 'location', 'about', 'user_skills']

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = companyprofile
        fields = ['image', 'email', 'tagline', 'location', 'about']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe your company...'}),
            'tagline': forms.TextInput(attrs={'placeholder': 'Company catchphrase'}),
        }

class JobForm(forms.ModelForm):
    custom_skills = forms.CharField(
        required=False,
        label="Required Skills",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. Django, Python, CSS',
            'class': 'form-control'
        })
    )

    class Meta:
        model = job
        fields = ['name', 'salary', 'jobtype', 'workmd', 'experience', 'description', 'expires_at']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
            'jobtype': forms.Select(attrs={'class': 'form-select'}),
            'workmd': forms.Select(attrs={'class': 'form-select'}),
            'experience': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'expires_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }