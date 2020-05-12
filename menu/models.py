from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)
    
    class Meta:
        ordering = ('id',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu:product_list_by_category',
                        args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                related_name='products',
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=20, blank=True)
    pizza_type = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ('id',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return f'{self.name} {self.category}'

    def get_absolute_url(self):
        return reverse('menu:product_detail', 
                        args=[self.id, self.slug])


# Create your models here.
# class Product(models.Model):
#     name = models.CharField(max_length=250)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     class Meta:
#         abstract = True


# class Topping(Product):
#     pass


# class Pizza(Product):
#     size = models.CharField(max_length=20)
#     category = models.CharField(max_length=50)
#     topping1 = models.ForeignKey(Topping, related_name="top1", 
#                                 null=True, blank=True, on_delete=models.SET_NULL)
#     topping2 = models.ForeignKey(Topping, related_name="top2",
#                                 null=True, blank=True, on_delete=models.SET_NULL)
#     topping3 = models.ForeignKey(Topping, related_name="top3",
#                                 null=True, blank=True, on_delete=models.SET_NULL)
#     topping4 = models.ForeignKey(Topping, related_name="top4",
#                                 null=True, blank=True, on_delete=models.SET_NULL)
#     topping5 = models.ForeignKey(Topping, related_name="top5",
#                                 null=True, blank=True, on_delete=models.SET_NULL)


# class Sub(Product):
#     size = models.CharField(max_length=20)


# class Pasta(Product):
#     pass


# class Salad(Product):
#     pass


# class DinnerPlatter(Product):
#     size = models.CharField(max_length=20)