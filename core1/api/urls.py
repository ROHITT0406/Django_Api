from home.views import index,person,login,PersonAPI,PeopleViewSet,RegisterAPI,LoginAPI
from django.urls import path,include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'people',PeopleViewSet,basename='people')
urlpatterns = router.urls

urlpatterns = [
    path('login/',LoginAPI.as_view()),
    path('',include(router.urls)),
    path('register/',RegisterAPI.as_view()),#class need .as_view() to run as views function 
    path('index/',index,name='index'),
    path('person/',person,name='person'),
    path('login/',login,name='login'),
    path('persons/',PersonAPI.as_view())
]
