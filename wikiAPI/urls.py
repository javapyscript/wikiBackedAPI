from django.conf.urls import url
from django.urls import path, include, re_path
from wikiAPI import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [

        path('documents/', include([
            path('', views.get_documents),
            path('<str:title>/', views.get_revisions_by_title),
            path('<str:title>/latest/', views.get_latest_version),
            path('<str:title>/<timestamp>/', views.get_doc_by_timestamp)
        ])),
        url(r'^addDocument/$',views.add_document),

]