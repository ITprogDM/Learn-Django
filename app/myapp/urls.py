from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('test/', test, name='test'),
    #path('', index, name='home'),
    path('', HomeMyapp.as_view(), name='home'),
    #path('category/<int:category_id>/', get_category, name='category'),
    path('category/<int:category_id>/', MyappByCategory.as_view(), name='category'),
    #path('myapp/<int:myapp_id>/', view_myapp, name='view_myapp'),
    path('myapp/<int:pk>/', ViewMyapp.as_view(), name='view_myapp'),
    #path('myapp/add-myapp/', add_myapp, name='add_myapp'),
    path('myapp/add-myapp/', CreateMyapp.as_view(), name='add_myapp'),
]