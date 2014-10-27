from django.conf.urls import patterns, url

from .views import FlagView
from .api import CreateFlag, RetrieveReason


urlpatterns = patterns('',
    url('^$', FlagView.as_view(), name='flaggit'),
)


# api url
urlpatterns += patterns('',
    url('^api/create$', CreateFlag.as_view(), name='api_create_flag'),
    url(r'^api/reason$', RetrieveReason.as_view(), name='api_retrieve_reason')
)
