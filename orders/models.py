from django.db import models
from menu.models import Product
from django.contrib.auth.models import User


# Create your models here.
class OrderItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, unique=False)
    # optional toppings and extras
    topping1 = models.ForeignKey(Product, on_delete=models.SET_NULL, unique=False,
                                 related_name="topping1", null=True, blank=True)
    topping2 = models.ForeignKey(Product, on_delete=models.SET_NULL, unique=False,
                                 related_name="topping2", null=True, blank=True)
    topping3 = models.ForeignKey(Product, on_delete=models.SET_NULL, unique=False,
                                 related_name="topping3", null=True, blank=True)
    extras1 = models.ForeignKey(Product, on_delete=models.SET_NULL, unique=False,
                                related_name="extras1", null=True, blank=True)
    extras2 = models.ForeignKey(Product, on_delete=models.SET_NULL, unique=False,
                                related_name="extras2", null=True, blank=True)
    extras3 = models.ForeignKey(Product, on_delete=models.SET_NULL, unique=False,
                                related_name="extras3", null=True, blank=True)
    extras4 = models.ForeignKey(Product, on_delete=models.SET_NULL, unique=False,
                                related_name="extras4", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quantity = models.PositiveIntegerField(default=0)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} ) {self.product.name} {self.product.category.name} of {self.owner.username}"

    def get_cost(self):
        """
        cost of an item
        """
        return self.price * self.quantity

    def get_toppings(self):
        """
        toppings
        """
        toppings = [t.name for t in [self.topping1, self.topping2, self.topping3] if (t)]
        return toppings

    def get_extras(self):
        """
        extras
        """
        extras = [e.name for e in [self.extras1, self.extras2, self.extras3, self.extras4] if (e)]
        return extras

    def get_add_ons(self):
        """
        return add ons information
        """
        toppings = self.get_toppings()
        extras = self.get_extras()

        if len(toppings) >= 1:
            return "with (" + ", ".join(toppings) + ") toppings"
        elif len(extras) >= 1:
            return "with (" + ", ".join(extras) + ") extras"
        else:
            return ""


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250, default="")
    items = models.ManyToManyField(OrderItem)
    paid = models.BooleanField(default=False)
    postal_code = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=250, default="")
    state = models.CharField(max_length=250, default="")
    country = models.CharField(max_length=2, default="")

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'Order {self.id} belongs to {self.owner.username}'

    def get_all_items(self):
        """
        get all items
        """
        return self.items.all()

    def mark_order_items(self):
        """
        mark order items as ordered after payment completion
        """
        if self.paid == True:
            for item in self.get_all_items():
                if item.quantity != 0:
                    item.ordered = True
                    item.save()

    def get_cart_items(self):
        """
        get items currently in cart
        """
        return self.items.filter(ordered=False, quantity__gt=0)

    def tot_quant_n_cost(self):
        """
        get total quantity and cost of items in cart
        """
        totalItems = 0
        totalCost = 0
        for item in self.get_cart_items():
            totalItems += item.quantity
            totalCost += item.get_cost()
        return totalItems, totalCost
