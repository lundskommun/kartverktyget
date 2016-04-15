from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from survey.models import Survey, Contribution


class SurveyAdmin(admin.ModelAdmin):
    def survey_public_link(obj):
        url = reverse('show_survey', args=[obj.slug])
        return '<a href="%s"><strong>%s</strong></a>' % (url, _('Link'))

    def survey_data_link(obj):
        url = reverse('show_results', args=[obj.slug])
        return '<a href="%s"><strong>%s</strong></a>' % (url, _('Link'))

    def save_model(self, req, obj, form, change):
        obj.owner = req.user
        obj.save()

    def get_queryset(self, request):
        qs = super(SurveyAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    survey_public_link.short_description = _('public link')
    survey_public_link.allow_tags = True

    survey_data_link.short_description = _('results link')
    survey_data_link.allow_tags = True

    prepopulated_fields = {
        'slug': ('title',)
    }

    exclude = ('owner', )

    list_display = ('title', 'published', survey_public_link, survey_data_link)


class ContributionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_filter = ('survey', 'created')
    list_display = ('created', 'survey')
    readonly_fields = ('survey', 'created', 'questionnaire_data', 'geometry_data', 'ip_address')

    def get_queryset(self, request):
        qs = super(ContributionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(survey__owner=request.user)


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Contribution, ContributionAdmin)
