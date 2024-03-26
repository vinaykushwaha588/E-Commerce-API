from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializers, UserLoginSerializers, ProductSerializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Product, CartItem
from .services import fetch_cart_items
from django.shortcuts import get_object_or_404


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
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        product_id = request.data.get('product_id')
        try:
            product = get_object_or_404(Product, pk=product_id)
            if 'cart' not in request.session:
                request.session['cart'] = {}

            cart = request.session['cart']

            if product_id in cart:
                cart[product_id]['quantity'] += 1
            else:
                cart[product_id] = {
                    'name': product.p_name,
                    'price': str(product.prize),
                    'quantity': 1,
                }
            request.session['cart'] = cart
            cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return Response({"success": False, 'message': "Items is Added in the the cart."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': err.args[0]})


class FetchCartItemView(APIView):
    permission_classes = (IsAuthenticated,)
    """
        This Views is used for the Fetch all Cart Item same User
    """

    def get(self, request, *args, **kwargs):
        cart_items = fetch_cart_items(request)
        return Response({'success': True, 'data': cart_items}, status=status.HTTP_200_OK)


class RemoveCartItemView(APIView):
    permission_classes = (IsAuthenticated,)
    """
        This View is used for the Remove Cart Items
    """

    def post(self, request, product_id):
        try:
            cart_items = request.session.get('cart', {})

            if str(product_id) in cart_items:
                del cart_items[str(product_id)]
                request.session['cart'] = cart_items
                return Response({'success': True, 'message': 'Item removed from cart successfully.'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'error': 'Product not found in cart.'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
