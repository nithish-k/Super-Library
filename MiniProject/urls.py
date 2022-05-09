from django.contrib import admin
from django.urls import path
from Library import views as vh
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('root/', admin.site.urls),
    path("", vh.home),
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
    path("publish_edit/<str:current_book>", vh.edit_publish),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
