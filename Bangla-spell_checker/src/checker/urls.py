from django.conf.urls import url

from .views import *
from django.urls import path
app_name='checker'

urlpatterns = [
	path('', index, name='index'),
	path('result', spell_check_result, name='result'),
	path('edit', edit_text, name='edit')
]
