from django.urls import path

from user import views

# App name as used in the unittests
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserAPIView.as_view(), name='create'),
    path('token/', views.CreateTokenAPIView.as_view(), name='token'),
    path('me/', views.ManageUserAPIView.as_view(), name='me')
]
