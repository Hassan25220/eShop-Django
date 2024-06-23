from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from products.models import Product, SizeVariant, Cart, CartItem
# Create your views here.



def get_product(request, slug):
    try:
        # Ya slug hum product k related slug or oski info ko open ketna k lya ker rha hai
        product = Product.objects.get(slug = slug)
        context = {'product': product}

        # jo size hum ne url ma show kerwaya hai ose backend ma save kerna k lya humne ya condition lgye hai
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size']= size
            context['updated_price'] = price
            print(price)

        return render(request, "product/product.html", context)
    
    
    except Product.DoesNotExist:
        return render(request, '404.html', status=404)
    except Exception as e:
        print(e)
        return render(request, '500.html', status=500)
    
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    size_name = request.POST.get('size')
    quantity = int(request.POST.get('quantity', 1))

    size_variant = None
    if size_name:
        size_variant = get_object_or_404(SizeVariant, size_name=size_name, product=product)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, size_variant=size_variant)

    if not created:
        cart_item.quantity += quantity
    cart_item.save()

    return HttpResponseRedirect(reverse('view_cart'))

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None
    return render(request, 'product/view_cart.html', {'cart': cart})


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    action = request.POST.get('action')

    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    elif action == 'remove':
        cart_item.delete()
        return redirect('view_cart')

    cart_item.save()
    return redirect('view_cart')