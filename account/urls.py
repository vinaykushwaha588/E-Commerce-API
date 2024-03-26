from django.urls import path
from account import views

urlpatterns = [
    path('register', views.RegisterUserView.as_view()),
    path('login', views.UserLoginView.as_view()),
    path('create-products', views.CreateProductView.as_view()),
    path('fetch-products', views.RetriveProductsView.as_view()),
    path('add-cart', views.AddToCartAPIView.as_view()),
    path('fetch/cart-item', views.FetchCartItemView.as_view()),
    path('remove/cart-item/<int:product_id>', views.RemoveCartItemView.as_view()),
]
