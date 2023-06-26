from rest_framework import generics
from .models import Product
from authentication.models import User
from .serializers import ProductSerializer, ProductDetailSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUserView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Product.objects.filter(username__username=username)

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'pk'

class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductDetailSerializer

    def perform_create(self, serializer):
        # Set the username to the user specified in the URL
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        serializer.save(username=user)

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.kwargs['username']
        return queryset.filter(username__username=username)
