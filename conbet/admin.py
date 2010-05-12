from models import Team, Group, Match, Round, Qualification, Bet
from django.contrib import admin

admin.site.register(Match)

class MatchInline(admin.TabularInline):
    model = Match
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('home', 'visitor', 'date', 'location'),
        }),
        ('Results', {
            'fields': ('home_goals', 'visitor_goals', 'winner'),
        }),
    )
    ordering = ('date', 'id')

class GroupAdmin(admin.ModelAdmin):
    inlines = [
        MatchInline,
    ]
    ordering = ('name',)

admin.site.register(Group, GroupAdmin)

class RoundAdmin(admin.ModelAdmin):
    ordering = ('stage', 'order')
admin.site.register(Round, RoundAdmin)

admin.site.register(Team)
admin.site.register(Qualification)
admin.site.register(Bet)

