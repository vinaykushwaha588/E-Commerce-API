def fetch_cart_items(request):
    cart = request.session.get('cart')
    return cart
