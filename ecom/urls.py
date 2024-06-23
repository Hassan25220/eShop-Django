"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static #static or media files k lya or ya settings k sath combine hota hai jis se user file upload kr sakta hai.
from django.conf import settings # Settings ko import kr rha hai t ke 'DEBUG', 'MEDIA_URL', and 'MEDIA_ROOT' ko use kr sakte
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # is ma hum static files ko add kerte hai urls k sath

urlpatterns = [
    path('', include('home.urls')),
    path('product/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    
]
if settings.DEBUG: # Check kerta hai project development mode hai k nhi (aghr hai tu True otherwise False)
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
# Uper wale urlpatterns: se hum static files (like CSS, JavaScript, and images) ko url pattern k sath append kerte hai. Is se hum ensure kerte hai k static file theak work ker rehi hai development mode ma.

urlpatterns += staticfiles_urlpatterns()