from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    notification_type = models.BooleanField(default=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class UserCard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.card_number}"

    class Meta:
        verbose_name = 'User Card'
        verbose_name_plural = 'User Cards'

class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    house_number = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user.username} - {self.house_number}, {self.street}, {self.city}"

    class Meta:
        verbose_name = 'User Address'
        verbose_name_plural = 'User Addresses'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveBigIntegerField()
    description = models.TextField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    view_count = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.color}"

    class Meta:
        verbose_name = 'Product Color'
        verbose_name_plural = 'Product Colors'

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.size}"

    class Meta:
        verbose_name = 'Product Size'
        verbose_name_plural = 'Product Sizes'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"{self.product.name} - {self.image}"

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product Rating'
        verbose_name_plural = 'Product Ratings'
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.product.name} - {self.rating}"

class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product Comment'
        verbose_name_plural = 'Product Comments'

    def __str__(self):
        return f"{self.product.name} - {self.comment[:20]}"

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f"{self.user.username} - Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.cart.user.username} - {self.product.name}"

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    card = models.ForeignKey(UserCard, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=[
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('delivered', 'Delivered')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"{self.user.username} - Order #{self.id}"

class PromoCode(models.Model):
    code = models.CharField(max_length=100)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Promo Code'
        verbose_name_plural = 'Promo Codes'
