from django.conf.urls import url

from views import show_survey, show_settings, post_contribution, prepare_form, show_results, get_features, export_excel, \
    export_geojson

urlpatterns = [
    url(r'(?P<slug>[\w-]+)/form', prepare_form, name='prepare_form'),
    url(r'(?P<slug>[\w-]+)/post', post_contribution, name='post_contribution'),
    url(r'(?P<slug>[\w-]+)/settings.js', show_settings, name='survey_settings'),
    url(r'(?P<slug>[\w-]+)/results/export_geojson$', export_geojson, name='export_geojson'),
    url(r'(?P<slug>[\w-]+)/results/export_excel$', export_excel, name='export_excel'),
    url(r'(?P<slug>[\w-]+)/results/features$', get_features, name='get_features'),
    url(r'(?P<slug>[\w-]+)/results$', show_results, name='show_results'),
    url(r'(?P<slug>[\w-]+)$', show_survey, name='show_survey'),
]
