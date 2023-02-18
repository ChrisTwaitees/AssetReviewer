from django.urls import path
from asset_viewer_app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path(r'', views.HomePageView.as_view(), name="index"),
    path(r'', views.AssetsHomepageView.as_view(), name="index")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


