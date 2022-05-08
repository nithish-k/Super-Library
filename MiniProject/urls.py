from django.contrib import admin
from django.urls import path
from Library import views as vh
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', admin.site.urls),
    path("", vh.home),
    path("collections/", vh.collections),
    path("login/", vh.login),
    path("logout/", vh.logout), 
    path("add/", vh.add),
    path("add/success", vh.add),
    path("add/fail", vh.add),
    path("readcode/", vh.readcode),
    path("student_scan/", vh.student_scan),
    path("student_scanner/", vh.student_scanner),
    path("borrow/<str:roll>", vh.borrow),
    path("add_book/<str:b_roll>", vh.add_book),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
