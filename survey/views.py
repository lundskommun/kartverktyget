import json
import time
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context_processors import csrf
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import ensure_csrf_cookie

from crawls import settings
from export_excel import export_to_excel
from export_geojson import export_to_geojson
from models import Survey, Contribution

FORM_CONFIGURATIONS = {
    Survey.QUESTIONNAIRE_FREE_TEXT: {
        'Point': ('survey/form_freetext.html', ['inputText', 'inputGeometry']),
        'LineString': ('survey/form_freetext.html', ['inputText', 'inputGeometry']),
        'Polygon': ('survey/form_freetext.html', ['inputText', 'inputGeometry']),
    },
    Survey.QUESTIONNAIRE_SCHOOL_TRIPS: {
        'Point': ('survey/form_freetext.html', ['inputText', 'inputGeometry']),
        'LineString': ('survey/form_school_line.html',
                       ['inputText', 'inputGeometry', 'inputMeans', 'inputHelmet', 'inputAge', 'inputDestination']),
    }
}


def ping(req):
    return render_to_response('survey/ping.txt')


def show_settings(req, slug):
    survey = get_object_or_404(Survey, slug=slug)

    if survey.questionnaire == Survey.QUESTIONNAIRE_FREE_TEXT:
        allow_polygons = 'true'
    else:
        allow_polygons = 'false'

    form_url = reverse('prepare_form', args=[slug])
    post_url = reverse('post_contribution', args=[slug])

    context = {
        'map_center': survey.map_center,
        'allow_polygons': allow_polygons,
        'form_url': form_url,
        'post_url': post_url,
        'raven_dsn': settings.RAVEN_DSN,
    }

    return render_to_response('survey/survey_settings.js.template', context)


def post_contribution(req, slug):
    survey = get_object_or_404(Survey, slug=slug)

    if not survey.published:
        return HttpResponseForbidden('Survey is closed')

    qd = {
        'text': req.POST['inputText']
    }

    # Don't make a full check, just make a sanity check
    if survey.questionnaire == Survey.QUESTIONNAIRE_SCHOOL_TRIPS and \
            req.POST.has_key('inputMeans') and req.POST.has_key('inputAge'):
        qd['means'] = req.POST['inputMeans']
        qd['helmet'] = req.POST['inputHelmet']
        qd['age'] = req.POST['inputAge']
        qd['destination'] = req.POST['inputDestination']

    # TODO: Error handling
    contribution = Contribution()
    contribution.survey = survey
    contribution.geometry_data = req.POST['inputGeometry']
    contribution.questionnaire_data = json.dumps(qd)
    contribution.ip_address = req.META['REMOTE_ADDR']
    contribution.save()

    rsp = {
        'success': True
    }

    time.sleep(1)
    return JsonResponse(rsp)


def prepare_form(req, slug):
    survey = get_object_or_404(Survey, slug=slug)

    geojson = json.loads(req.POST['feature'])

    config = FORM_CONFIGURATIONS[survey.questionnaire]
    template_name, fields = config[geojson['geometry']['type']]
    template = get_template(template_name)

    template_context = {
        'geometry_data': req.POST['feature'],
    }

    rsp = {
        'fragment': template.render(template_context),
        'fields': fields,
    }

    return JsonResponse(rsp)

@ensure_csrf_cookie
def show_survey(req, slug):
    survey = get_object_or_404(Survey, slug=slug)

    # Bail out if not published
    if not survey.published:
        return render_to_response('survey/survey_not_published.html')

    # Continue
    context = {
        'survey': survey,
        'contact_email': settings.CONTACT_EMAIL,
        'google_analytics_key': settings.GOOGLE_ANALYTICS_KEY,
    }

    context.update(csrf(req))
    return render_to_response('survey/survey.html', context)


def _is_line(contribution):
    geo = json.loads(contribution.geometry_data)
    return geo['geometry']['type'] == 'LineString'


def _is_point(contribution):
    geo = json.loads(contribution.geometry_data)
    return geo['geometry']['type'] == 'Point'


def _is_polygon(contribution):
    geo = json.loads(contribution.geometry_data)
    return geo['geometry']['type'] == 'Polygon'


def _get_predicate(type_string):
    lookup_table = {
        'point': _is_point,
        'linestring': _is_line,
        'polygon': _is_polygon
    }

    return lookup_table[type_string]


def _filter_contributions(contributions, req):
    type_ = req.GET['type'].lower()
    predicate = _get_predicate(type_)
    return filter(predicate, contributions), type_


def export_geojson(req, slug):
    survey = get_object_or_404(Survey, slug=slug)

    # Bail out if not allowed to access
    if not (req.user.is_superuser or req.user == survey.owner):
        return render_to_response('survey/results_not_allowed.html')

    # Filter out contributions
    contributions, type_ = _filter_contributions(survey.contribution_set.all(), req)

    # Generate response
    payload = export_to_geojson(contributions)
    filename = '%s_%s.geojson' % (slug, type_)
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="%s"' % (filename,)
    response.write(payload)
    return response


def export_excel(req, slug):
    survey = get_object_or_404(Survey, slug=slug)

    # Bail out if not allowed to access
    if not (req.user.is_superuser or req.user == survey.owner):
        return render_to_response('survey/results_not_allowed.html')

    # Filter out contributions
    contributions, type_ = _filter_contributions(survey.contribution_set.all(), req)

    # Generate response
    payload = export_to_excel(contributions)
    filename = '%s_%s.xlsx' % (slug, type_)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % (filename,)
    response.write(payload)
    return response


@login_required
@ensure_csrf_cookie
def show_results(req, slug):
    survey = get_object_or_404(Survey, slug=slug)

    # Bail out if not allowed to access
    if not (req.user.is_superuser or req.user == survey.owner):
        return render_to_response('survey/results_not_allowed.html')

    # Continue
    contributions = survey.contribution_set.all()
    context = {
        'survey': survey,
        'point_count': len(filter(_is_point, contributions)),
        'line_count': len(filter(_is_line, contributions)),
        'polygon_count': len(filter(_is_polygon, contributions)),
        'google_analytics_key': settings.GOOGLE_ANALYTICS_KEY,
    }

    return render_to_response('survey/results.html', context)


def _take_words(text, word_count):
    words = text.split()
    total_word_count = len(words)
    if total_word_count > word_count:
        return u' '.join(words[:20]) + _(' [...] (truncated)')
    else:
        return u' '.join(words)


def _to_geojson_for_overview(contribution):
    questionnaire = json.loads(contribution.questionnaire_data)
    geo = json.loads(contribution.geometry_data)
    id_ = _('ID %d') % contribution.id
    text = _take_words(questionnaire['text'], 20)
    geo['properties']['description'] = '%s: %s' % (id_, text)
    return json.dumps(geo)


def get_features(req, slug):
    survey = get_object_or_404(Survey, slug=slug)

    # Bail out if not allowed to access
    if not (req.user.is_superuser or req.user == survey.owner):
        return HttpResponseForbidden()

    # Continue
    contributions = survey.contribution_set.all()
    geojson_array = '[ %s ]' % ','.join(map(_to_geojson_for_overview, contributions))
    return HttpResponse(geojson_array, 'application/json')
