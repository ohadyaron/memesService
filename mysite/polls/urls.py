from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
                  path('', views.IndexView.as_view(), name='index'),
                  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
                  path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
                  path('<int:pk>/image', views.ImageView.as_view(), name='image'),
                  path('<int:pk>/meme/', views.MemView.as_view(), name='meme'),
                  path('<int:pk>/set_text/', views.set_text, name='set_text'),
                  path('<int:question_id>/vote/', views.vote, name='vote'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
