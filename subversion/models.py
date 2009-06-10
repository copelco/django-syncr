# SubversionSyncr - 0.0.2
#
# Author:  Maxime Haineault <haineault@gmail.com>
# License: MIT License ~ http://www.opensource.org/licenses/mit-license.php
# Documentation: http://code.google.com/p/django-syncr/wiki/SyncrSubversion


from django.db import models

class SubversionSync(models.Model):
    url = models.CharField(max_length=250, blank=False)
    username  = models.CharField(max_length=50, blank=True)
    password  = models.CharField(max_length=50, blank=True)
    rev_start = models.PositiveIntegerField(null=True, blank=True)
    rev_end   = models.PositiveIntegerField(null=True, blank=True)     
    limit     = models.PositiveIntegerField(default=1000, blank=True) 
    discover_changed_paths = models.BooleanField(default=False) # WARNING: Will take significantly longer to sync if set to True
    peg_revision = models.PositiveIntegerField(null=True, blank=True) # I have no idea what's this
    include_merged_rev = models.BooleanField(default=False)
    strict_node_history = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.url

class Revision(models.Model):
    revision      = models.PositiveIntegerField()
    svnPath       = models.CharField(max_length=250, blank=True) # act as a "slug"
    date          = models.DateTimeField(blank=True, null=True)
    message       = models.TextField(blank=True)
    changed_paths = models.TextField(blank=True) # JSON
    author        = models.CharField(max_length=250, blank=True, default='') # unrelated to django.auth.users
    revision_kind = models.CharField(max_length=50, blank=True, default="number")
    has_children  = models.CharField(blank=True, max_length=250)

    class Meta:
        unique_together = ("revision", "svnPath")
        ordering = ["-date"]

    def __unicode__(self):
        return u'r%s - %s' % (self.revision, self.message, )
