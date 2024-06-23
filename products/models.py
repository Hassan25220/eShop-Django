from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Import kya hai 'base' wala 'models.py' t ka hum ise entire project ma use ker sake
from base.models import BaseModel

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)  # ya url ma name ki madad se page open kerwane ma help kerti hai
    category_image = models.ImageField(upload_to="categories")

    # Is ma hum slug create kr rha hai (slug mutlab: jab bhi hum koi product search kare tu urls ma product k title a jata hai (eg: home/products/tooth-paste))
    def save(self, *args, **kwargs): # def save() wo function hai jo har bar call hota hai jab bhi koi program run hota hai.
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name


class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color_name

class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.size_name


class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    product_description = models.TextField()
    color_variant = models.ManyToManyField(ColorVariant, blank = True)
    size_variant = models.ManyToManyField(SizeVariant,related_name="product" ,blank = True)

    def save(self, *args, **kwargs): # def save() wo function hai jo har bar call hota hai jab bhi koi program run hota hai.
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name
    
    def get_product_price_by_size(self, size):
        try:
            size_variant = self.size_variant.get(size_name=size)
            return self.price + size_variant.price
        except SizeVariant.DoesNotExist:
            return self.price
    

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to="product")


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)

# Cart model
class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart ({self.user.username})"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

# CartItem model
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        size = f" (Size: {self.size_variant.size_name})" if self.size_variant else ""
        return f"{self.product.product_name}{size} x {self.quantity}"

    def get_total_price(self):
        base_price = self.product.price
        if self.size_variant:
            base_price += self.size_variant.price
        return base_price * self.quantity




