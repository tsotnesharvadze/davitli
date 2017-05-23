from django.contrib import admin
from django.conf.urls import url, include
from .views import Index
urlpatterns = [
    url(r'^66d2b8f4a09cd75cb23076a1da5d51529136a3373fd570b122/?$', Index.as_view()), 
]