from django.db import models

class GoogleCodeSvnChange(models.Model):
    date_updated  = models.DateTimeField()
    subtitle      = models.TextField()
    link          = models.CharField(max_length=250)
    title         = models.CharField(max_length=250)
    project       = models.CharField(max_length=50)
    author        = models.CharField(max_length=50)
    rev           = models.PositiveIntegerField()

    def __unicode__(self):
        return u'%s' % self.rev


class GoogleCodeProjectDownload(models.Model):
    date_updated  = models.DateTimeField()
    subtitle      = models.TextField()
    link          = models.CharField(max_length=250)
    title         = models.CharField(max_length=250)
    project       = models.CharField(max_length=50)
    author        = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.rev

