from .cart import Cart


def card(request):
    return {'cart': Cart(request)}
