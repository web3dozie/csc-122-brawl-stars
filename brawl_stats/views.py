from django.views.generic import ListView
from .models import Brawler, TierList

class BrawlerListView(ListView):
    model = Brawler
    template_name = 'brawl_stats/brawler_list.html'
    context_object_name = 'brawlers' 
    # queryset = Brawler.objects.order_by('name')

class TierListListView(ListView):
    model = TierList
    template_name = 'brawl_stats/tierlist_list.html'
    context_object_name = 'tierlists'
    # queryset = TierList.objects.select_related('author').order_by('-created_at')
