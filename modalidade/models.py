from django.db import models

class Modalidade(models.Model):
    desc = models.CharField(max_length='100',blank=False, null=False)
	
    def __unicode__(self):
        return u'%s' % (self.id)