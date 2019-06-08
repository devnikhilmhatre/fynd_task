from django.urls import path

from .views import SignIn, SignOut

urlpatterns = [
    path('login/', SignIn.as_view()),
    path('logout/', SignOut.as_view())
]
