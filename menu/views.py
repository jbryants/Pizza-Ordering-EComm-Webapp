from django.views.generic import ListView, DetailView
from .models import Category, Product
from django.shortcuts import get_object_or_404


class ProductListView(ListView):
    template_name = "menu/product/list.html"
    context_object_name = "category_list"
    model = Category

    def get_context_data(self, **kwargs):
        category = None
        # exclude toppings and extras in products
        products = Product.objects.exclude(price__in=[0.0, 0.50])
        toppings = Product.objects.filter(price=0.0)
        extras = Product.objects.filter(price=0.50)
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            # if /category/ page then filter products by category
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        context = super().get_context_data(**kwargs)
        # currently selected category and product list
        context['category'] = category
        context['product_list'] = products
        context['toppings_list'] = toppings
        context['extras_list'] = extras
        return context

    def get_queryset(self):
        # all categories list except toppings and extras
        return Category.objects.exclude(name__in=["Toppings", "Extras"])


class ProductDetailView(DetailView):
    template_name = "menu/product/details.html"

    def get_object(self):
        # detail view based on id and slug of product selected.
        id_ = self.kwargs.get("id")
        slug_ = self.kwargs.get("slug")
        return get_object_or_404(Product, id=id_, slug=slug_)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        toppings = Product.objects.filter(price=0.0)
        extras = Product.objects.filter(price=0.50)
        context['toppings_list'] = toppings
        context['extras_list'] = extras
        return context
