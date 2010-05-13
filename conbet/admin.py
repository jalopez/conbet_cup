from models import Team, Group, GroupMatch, Round, Qualification, Bet
from django.contrib import admin


class GroupMatchesInline(admin.TabularInline):
    model = GroupMatch
    extra = 0
    fieldsets = (
        ('Match', {
            'fields': ('home', 'visitor', 'date', 'location'),
        }),
        ('Results', {
            'fields': ('home_goals', 'visitor_goals', 'winner'),
        }),
    )
    ordering = ('date', 'id')

class GroupAdmin(admin.ModelAdmin):
    inlines = [
        GroupMatchesInline,
    ]
    ordering = ('name',)

admin.site.register(Group, GroupAdmin)

class RoundAdmin(admin.ModelAdmin):
    ordering = ('stage', 'order')
    fieldsets = (
        (None, {
            'fields': ('stage', 'order'),
        }),
        ('Match', {
            'fields': ('home', 'visitor', 'date', 'location'),
        }),
        ('Results', {
            'fields': ('home_goals', 'visitor_goals', 'winner'),
        }),
    )
        
admin.site.register(Round, RoundAdmin)

admin.site.register(Team)
admin.site.register(Qualification)
admin.site.register(Bet)
