from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from checkins.views import home, get_form, report

urlpatterns = [
    path('', home),
    path('check-in/', get_form),
    path('report/', report, name='report')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
