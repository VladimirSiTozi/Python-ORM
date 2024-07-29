from django.contrib import admin

from main_app.models import FootballPlayer, FootballCoach, League, Team


# Register your models here.

@admin.register(FootballPlayer)
class FootballPlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'nationality',)
    search_fields = ('full_name', 'nationality', )


@admin.register(FootballCoach)
class FootballCoachAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'nationality',)
    search_fields = ('full_name', 'nationality', )


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'prize_money', 'start_date')
    list_filter = ('name', )
    search_fields = ('name', 'team__name')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'fans', 'stadium')
    list_filter = ('name', )
    search_fields = ('name', 'stadium')
