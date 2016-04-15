from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Survey(models.Model):
    QUESTIONNAIRE_FREE_TEXT = 'F'
    QUESTIONNAIRE_SCHOOL_TRIPS = 'S'

    QUESTIONNAIRES = (
        (QUESTIONNAIRE_FREE_TEXT, _('Free-text')),
        (QUESTIONNAIRE_SCHOOL_TRIPS, _('School trips (original crawls)')),
    )

    def __init__(self, *args, **kwargs):
        super(Survey, self).__init__(*args, **kwargs)
        self._current_questionnaire = self.questionnaire

    created = models.DateTimeField(
        _('created'),
        auto_now_add=True
    )
    title = models.CharField(
        _('title'),
        help_text=_('This title is shown to all users.'),
        max_length=60,
    )
    slug = models.SlugField(
        _('slug'),
        help_text=_('Slug, or short-name. Used in URLs. Needs to be unique.'),
        unique=True)
    owner = models.ForeignKey(
        User,
        verbose_name=_('user'),
        help_text=_('This is the user currently owning this survey. If you change this to someone else, and you are \
                     not a super-user, then you will not be able to see the survey any longer.'))
    description = RichTextField(
        _('description'),
        help_text=_('This description is show to the contributors.'),
        blank=True,
    )
    map_center = models.CharField(
        _('map center'),
        help_text=_('Map center is where to center the map when the user first arrives. ' +
                    'Defaults to 55.7053, 13.1865 (central Lund).'),
        max_length=32,
        default='55.7053, 13.1865',
    )
    published = models.BooleanField(
        _('published'),
        help_text=_('Decides if the survey should be available to contributors.'),
        default=False,
    )
    questionnaire = models.CharField(
        _('questionnaire'),
        help_text=_('Decides which questionnaire to use.'),
        max_length=1,
        choices=QUESTIONNAIRES,
        default=QUESTIONNAIRE_FREE_TEXT,
    )
    image = models.ImageField(
        _('image'),
        help_text=_('Image to be shown in conjunction with your survey.'),
        blank=True
    )

    def clean(self):
        if (self._current_questionnaire != self.questionnaire) and self.contribution_set.exists():
            raise ValidationError(_('Cannot modify questionnaire. Survey already has contributions.'))

    def __unicode__(self):
        return u'%s' % (self.title,)

    class Meta:
        verbose_name = _('survey')
        verbose_name_plural = _('surveys')


class Contribution(models.Model):
    created = models.DateTimeField(
        _('created'),
        auto_now_add=True)
    survey = models.ForeignKey(
        Survey,
        verbose_name=_('survey'))
    questionnaire_data = models.TextField(
        _('questionnaire data'),
        help_text=_('This is the stored responses from the contribution. Not to be edited.')
    )
    geometry_data = models.TextField(
        _('geometry data'),
        help_text=_('This is the stored geoemetry from the contribution. Not to be edited.')
    )
    ip_address = models.GenericIPAddressField(
        _('IP address'),
        help_text=_('This is the IP address that the contribution originated from.')
    )

    def __unicode__(self):
        return _('Contribution from %s') % (self.ip_address,)

    class Meta:
        verbose_name = _('contribution')
        verbose_name_plural = _('contributions')
