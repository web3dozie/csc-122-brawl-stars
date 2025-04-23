from django.urls import path
from . import views

app_name = 'brawl_stats' 

urlpatterns = [
    path('brawlers/', views.BrawlerListView.as_view(), name='brawler_list'),
    path('tierlists/', views.TierListListView.as_view(), name='tierlist_list'),
    # TODO add paths for other views later
]