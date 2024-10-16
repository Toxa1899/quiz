from ast import parse

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from applications.account import views
from applications.account.views import TelegramLoginView, tg

urlpatterns = [
    path('user/', TelegramLoginView.as_view()),
    path('tg/', views.tg),
    # path('index', views.index),
# path('callback', views.callback),
# path('redirect', views.redirect),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)