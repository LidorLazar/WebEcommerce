from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('users/login/', views.MyTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('products/', views.get_products),
    path('products/<int:pk>', views.get_products_id),
    path('users/profile/', views.get_user_profile),
    path('users/', views.get_users),
    path('users/register/', views.register),
    path('category/<int:pk>', views.product_from_category),
    path('users/profile/update/', views.updateUserProfile),
    path('users/login/refresh/', views.RefreshTokenView.as_view()),
    path('products/sreview/', views.send_review),
    path('products/greview/<int:pk>', views.get_review_spsific_prod),
    path('products/getallreview/', views.get_all_review),

]
