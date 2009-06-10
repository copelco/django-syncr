from django.contrib import admin
from syncr.subversion.models import Revision


class RevisionAdmin(admin.ModelAdmin):
    list_display  = ('revision', 'message', 'author', 'date', 'svnPath')
    list_filter   = ('author', 'date', 'svnPath')
    search_fields = ['message', 'author', 'revision']
    date_hierarchy = 'date'
admin.site.register(Revision, RevisionAdmin)
