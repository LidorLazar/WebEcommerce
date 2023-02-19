from django.urls import path
from . import views


urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('products/', views.get_all_products),
    path('products/<int:pk>', views.get_products_id),
    path('users/profile/', views.get_user_profile),
    path('users/register/', views.register),
    path('category/<int:pk>', views.product_from_category),
    path('users/profile/update/', views.update_user_profile),
    path('users/login/refresh/', views.RefreshTokenView.as_view()),
    path('products/sreview/', views.send_review),
    path('products/greview/<int:pk>', views.get_review_spsific_prod),
    path('users/orders/', views.get_order_user),
    path('users/orders/product/', views.return_all_product_in_order_user),
    path('users/checkout/', views.create_new_order),


]
