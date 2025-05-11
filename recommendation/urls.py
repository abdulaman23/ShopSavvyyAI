from django.urls import path
from .views import get_recommendations, chatbot_reply

urlpatterns = [
    path('recommend/', get_recommendations, name='recommendation'),
    path('chat/', chatbot_reply, name='chatbot'),

]
