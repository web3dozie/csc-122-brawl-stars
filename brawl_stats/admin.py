from django.contrib import admin
from .models import GameMode, Map, Brawler, TierList, TierListEntry

@admin.register(GameMode)
class GameModeAdmin(admin.ModelAdmin):
    list_display = ('name', 'objective')
    search_fields = ('name', 'description', 'objective')

@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'game_mode', 'environment')
    search_fields = ('name', 'environment')
    list_filter = ('game_mode', 'environment')
    autocomplete_fields = ['game_mode']

@admin.register(Brawler)
class BrawlerAdmin(admin.ModelAdmin):
    list_display = ('name', 'rarity', 'brawler_type')
    search_fields = ('name', 'description')
    list_filter = ('rarity', 'brawler_type')


class TierListEntryInline(admin.TabularInline):
    model = TierListEntry
    extra = 1 # Number of empty forms to display
    autocomplete_fields = ['brawler']
    fields = ('brawler', 'tier', 'notes') # Control field order/visibility

@admin.register(TierList)
class TierListAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'author__username')
    list_filter = ('created_at', 'author')
    readonly_fields = ('created_at', 'updated_at') # Prevent editing timestamps
    autocomplete_fields = ['author']
    inlines = [TierListEntryInline] # Embed entries within the TierList admin page
    fieldsets = (
        (None, {
            'fields': ('name', 'author', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) # Make this section collapsible
        }),
    )

# Optional: Register TierListEntry directly if needed for standalone management
# @admin.register(TierListEntry)
# class TierListEntryAdmin(admin.ModelAdmin):
#     list_display = ('tier_list', 'brawler', 'tier')
#     search_fields = ('tier_list__name', 'brawler__name', 'notes')
#     list_filter = ('tier',)
#     autocomplete_fields = ['tier_list', 'brawler']
