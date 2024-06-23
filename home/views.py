from django.shortcuts import render
from products.models import Product
# Create your views here.

def index(request):
    # Humne jo bhi products or category create ki hai jango admin ki madad se ose show kerwane k lya hum ya 'context' create kr rha hai. Or hum is context ko ab index page pr use kr k show kerwaye gy
    context = {'products': Product.objects.all()}  
    return render(request, 'home/index.html', context)

