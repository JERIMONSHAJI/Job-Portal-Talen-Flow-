from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homefn),
    path('login/',loginfn),
    path('register/',registerfn),
    path('findjob/',findjobfn),
    path('view/<int:pid>/',viewfn),
    path('profile/',profilefn),
    path('dashboard/',dashboardfn),
    path('logout/',logoutfn),
    path('applay/<int:jid>/',applayfn),
    path('edit/<int:jid>/',editfn),
    path('editprofile/',editprofilefn),
    path('addjob/',addjobfn),
    path('delete/<int:jid>/',deletefn),
    path('applicants/<int:jid>/',viewapplicantsfn),
    path('update_status/<int:aid>/<str:status>/',update_status_fn),
    path('profile/<int:pk>/',profile_view),
    path('contactus/',contactusfn)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)