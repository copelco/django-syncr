# SubversionSyncr - 0.0.2
#
# Author:  Maxime Haineault <haineault@gmail.com>
# License: MIT License ~ http://www.opensource.org/licenses/mit-license.php
# Documentation: http://code.google.com/p/django-syncr/wiki/SyncrSubversion


from django.db import models

class Revision(models.Model):
    revision      = models.CharField(max_length=50, default="unknown")
    svnPath       = models.CharField(max_length=250, blank=True) # act as a "slug"
    date          = models.DateTimeField(blank=True, null=True)
    message       = models.TextField(blank=True)
    changed_paths = models.TextField(blank=True) # JSON
    author        = models.CharField(max_length=250, blank=True, default='') # unrelated to django.auth.users
    revision_kind = models.CharField(max_length=50, blank=True, default="number")
    has_children  = models.CharField(blank=True, max_length=250)

    class Meta:
        unique_together = ("revision", "svnPath")
        ordering = ['-date']

    def __unicode__(self):
        return u'r%s - %s' % (self.revision, self.message, )
