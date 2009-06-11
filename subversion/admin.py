from django.contrib import admin
from syncr.subversion.models import Revision, SubversionSync


class SubversionSyncAdmin(admin.ModelAdmin):
    list_display   = ('url', 'username', 'rev_start', 'rev_end', 'limit', 'include_merged_rev', 'discover_changed_paths')
    list_filter    = ('username',)
    search_fields  = ['url', 'username',]
admin.site.register(SubversionSync, SubversionSyncAdmin)

class RevisionAdmin(admin.ModelAdmin):
    list_display   = ('revision', 'message', 'author', 'date', 'svnPath')
    list_filter    = ('author', 'date', 'svnPath')
    search_fields  = ['message', 'author', 'revision']
    date_hierarchy = 'date'
    actions = []
admin.site.register(Revision, RevisionAdmin)
