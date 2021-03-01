from django.urls import path, include

from .views import (
     AreaListView, AreaCreate, AreaUpdate, AreaDelete,  LoginView
)

#, PlaceCreate, PlaceUpdate, PlaceDelete,RouteListView, RouteCreate,
  #  RouteUpdate, RouteDelete, 
urlpatterns = [
    path('area/', AreaListView.as_view(), name='area-list'),
    path('area/create/', AreaCreate.as_view(), name='area-create'),
    path('area/update/<int:pk>', AreaUpdate.as_view(), name='area-update'),
    path('area/delete/<int:pk>', AreaDelete.as_view(), name='area-delete'),
    path('geo/accounts/login', LoginView.as_view(), name='login'),
    
    
      
]
