

from django.urls import path, re_path
from apps.home import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('file-transfer', views.transfer, name='transfer'),

    path('get-file/<str:id>', views.get_file, name='get_file'),

    path('upload-done', views.upload_done, name='upload_done'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
