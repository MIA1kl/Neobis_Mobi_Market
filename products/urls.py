from django.urls import path
from products.views import ProductListView, ProductUserView, ProductDetailView, ProductCreateView, ProductDeleteView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/myproduct/<str:username>/', ProductUserView.as_view(), name='product-user'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/myproduct/<str:username>/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/myproduct/<str:username>/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

]
