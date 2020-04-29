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
'''

    path('create/', PlaceCreate.as_view(), name='place-create'),
    path('update/<int:pk>', PlaceUpdate.as_view(), name='place-update'),
    path('delete/<int:pk>', PlaceDelete.as_view(), name='place-delete'),
    path('route/', RouteListView.as_view(), name='route-list'),
    path('route/create/', RouteCreate.as_view(), name='route-create'),
    path('route/update/<int:pk>', RouteUpdate.as_view(), name='route-update'),
    path('route/delete/<int:pk>', RouteDelete.as_view(), name='route-delete')
    '''