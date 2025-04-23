from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class GameMode(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    objective = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Map(models.Model):
    name = models.CharField(max_length=100, unique=True)
    game_mode = models.ForeignKey(GameMode, on_delete=models.CASCADE, related_name='maps')
    environment = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(blank=True, null=True) # Optional image link

    def __str__(self):
        return f"{self.name} ({self.game_mode.name})"

    class Meta:
        ordering = ['game_mode', 'name']

class Brawler(models.Model):
    class Rarity(models.TextChoices):
        COMMON = 'CO', _('Common')
        RARE = 'RA', _('Rare')
        SUPER_RARE = 'SR', _('Super Rare')
        EPIC = 'EP', _('Epic')
        MYTHIC = 'MY', _('Mythic')
        LEGENDARY = 'LE', _('Legendary')

    class BrawlerType(models.TextChoices):
        DAMAGE_DEALER = 'DD', _('Damage Dealer')
        TANK = 'TK', _('Tank')
        ASSASSIN = 'AS', _('Assassin')
        SUPPORT = 'SU', _('Support')
        CONTROLLER = 'CN', _('Controller')
        ARTILLERY = 'AR', _('Artillery')

    name = models.CharField(max_length=100, unique=True)
    rarity = models.CharField(max_length=2, choices=Rarity.choices, default=Rarity.COMMON)
    brawler_type = models.CharField(max_length=2, choices=BrawlerType.choices)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True) # Optional image link

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class TierList(models.Model):
    name = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tier_lists')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Brawlers linked via TierListEntry

    def __str__(self):
        author_name = self.author.username if self.author else "Unknown"
        return f"{self.name} by {author_name}"

    class Meta:
        ordering = ['-created_at']

class TierListEntry(models.Model):
    class TierRating(models.TextChoices):
        S_TIER = 'S', _('S Tier')
        A_TIER = 'A', _('A Tier')
        B_TIER = 'B', _('B Tier')
        C_TIER = 'C', _('C Tier')
        D_TIER = 'D', _('D Tier')
        F_TIER = 'F', _('F Tier')

    tier_list = models.ForeignKey(TierList, on_delete=models.CASCADE, related_name='entries')
    brawler = models.ForeignKey(Brawler, on_delete=models.CASCADE, related_name='tier_entries')
    tier = models.CharField(max_length=1, choices=TierRating.choices)
    notes = models.TextField(blank=True, help_text="Optional notes about this brawler's placement.")

    def __str__(self):
        return f"{self.brawler.name} - {self.tier} ({self.tier_list.name})"

    class Meta:
        unique_together = ('tier_list', 'brawler') # A brawler can only appear once per tier list
        ordering = ['tier_list', 'tier', 'brawler']
