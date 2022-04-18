from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import MessageView


app_name='kblock'  

urlpatterns = [
	#Leave as empty string for base url
    path('', views.index , name="index"),
    path('account', views.account , name="account"),
    path('accounts/login', views.login_page, name='login'),
    path('accounts/register', views.register_page, name='register'),
    path('pdf/', MessageView.as_view(), name='createpdf'),
    path('commonarea', views.commonarea , name="common"), 
    path('checkhash', views.checkhash , name="checkhash"), 



    #path('pdf/', GeneratePdf.as_view()), 
    # Django Auth
    #path('accounts/login', auth_views.LoginView.as_view(template_name='accounts\login.html'), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(template_name=''), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)