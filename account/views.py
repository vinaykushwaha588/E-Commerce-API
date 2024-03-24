from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializers, UserLoginSerializers, ProductSerializers, AddToCartSerializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Product


# Create your views here.

class RegisterUserView(APIView):
    """
        This View is used for the Register User
    """

    def post(self, request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': True, 'message': 'User Register Successfully.'}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': serializer.error_messages}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
        This View is used for the login User.
    """

    def post(self, request):
        serializer = UserLoginSerializers(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            return Response({'success': True, 'refresh': user['refresh'], "access": user['access'],
                             }, status=status.HTTP_200_OK)
        return Response({'success': False, "error": serializer.error_messages, "messages": "invalid credential"},
                        status=status.HTTP_400_BAD_REQUEST)


class CreateProductView(APIView):
    """
        In This View is used for the create products ADMIN only.
    """
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializers(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': True, 'message': "Products Created Successfully."},
                            status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)


class RetriveProductsView(APIView):
    """
        This View is used for the Fetch Products.
        if you are sending category on the query params then you fetch all item in same category.
        without category fetch all ITEMS
    """

    def get(self, request):
        category = request.query_params.get('category')
        if category:
            product = Product.objects.filter(cat=category)
            serializer = ProductSerializers(product, many=True)
        else:
            query_set = Product.objects.all()
            serializer = ProductSerializers(query_set, many=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)


class AddToCartAPIView(APIView):
    def post(self, request):
        serializer = AddToCartSerializers(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']

            if 'cart' not in request.session:
                request.session['cart'] = {}
            if str(product_id) in request.session['cart']:
                request.session['cart'][str(product_id)] += quantity
            else:
                request.session['cart'][str(product_id)] = quantity

            return Response({"success": True, "message": "Item added to cart"}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)


class FetchCartItemView(APIView):
    permission_classes = (IsAuthenticated,)
    """
        This Views is used for the Fetch all Cart Item same User
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        cart_items = self.get_cart_items(user)

        serializer = AddToCartSerializers(cart_items, many=True)
        return Response(serializer.data)

    def get_cart_items(self, user):
        cart_items = user.cart_items.all()
        return cart_items
