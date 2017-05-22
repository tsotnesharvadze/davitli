from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField
# from sorl.thumbnail import get_thumbnail

# from random import randint
# from django.db.models import Q
# from django.utils import timezone

class AbsTime(models.Model):
	created = models.DateTimeField(_('შეიქმნა'), auto_now_add=True, null=True)
	updated = models.DateTimeField(_('განახლდა'), auto_now=True, null=True)

	class Meta:
		abstract = True

class Question(AbsTime):
	question = models.CharField(_('შეკითხვა'), max_length=200)
	mix = models.ForeignKey("QuestionMix", null=True,blank = True)
	class Meta:
		verbose_name = _('შეკითხვა')
		verbose_name_plural = _('შეკითხვები')

class Answer(AbsTime):
	answer = models.TextField(_('პასუხი'),null=True,blank=True)
	mix = models.ForeignKey("QuestionMix", null=True,blank = True)
	class Meta:
		verbose_name = _('პასუხი')
		verbose_name_plural = _('პასუხები')

class QuestionMix(AbsTime):
	FUNCTION_CHOICES=( (0,_('ფუნქციას არ იძახებს')),
			  )
	function = models.IntegerField(_('გამოსაძახებელი ფუნქცია'),choices = FUNCTION_CHOICES,default = 0,blank=True)

	def __str__(self):
		return self.question_set.first().question

	class Meta:
		verbose_name = _('კითხვა - პასუხი')
		verbose_name_plural = _('კითხვა - პასუხები')