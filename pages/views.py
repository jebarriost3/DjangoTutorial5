from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render, redirect


# ===========================
# Home Page View
# ===========================
class HomePageView(TemplateView):
    template_name = "pages/home.html"


# ===========================
# About Page View
# ===========================
class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Your Name",
        })
        return context


# ===========================
# Contact Page View
# ===========================
class ContactPageView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact Us - Online Store",
            "subtitle": "Contact Information",
            "email": "info@onlinestore.com",
            "address": "123 Main Street, Medellín, Colombia",
            "phone": "+57 300 123 4567",
        })
        return context


# ===========================
# Product Model (Simulated)
# ===========================
class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 499.99},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 999.99},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 29.99},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 79.99},
    ]



# ===========================
# Product Index View
# ===========================
class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.products,
        }
        return render(request, self.template_name, viewData)


# ===========================
# Product Show View
# ===========================
from django.http import HttpResponseRedirect
from django.urls import reverse

class ProductShowView(View):
    template_name = "products/show.html"

    def get(self, request, id):
        product_id = int(id) - 1  # Convertir el ID a índice de lista

        # Validar si el ID del producto es válido
        if 0 <= product_id < len(Product.products):
            product = Product.products[product_id]
            viewData = {
                "title": product["name"] + " - Online Store",
                "subtitle": product["name"] + " - Product information",
                "product": product,
            }
            return render(request, self.template_name, viewData)
        
        # Si el ID no es válido, redirigir a home
        return HttpResponseRedirect(reverse('home'))


# ===========================
# Product Form
# ===========================
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True, min_value=0.01) 

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("The price must be greater than zero.")
        return price



# ===========================
# Product Create View
# ===========================
class ProductCreateView(View):
    template_name = "products/create.html"

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {"title": "Create product", "form": form})

    def post(self, request):
        form = ProductForm(request.POST)

        if form.is_valid():
            return render(request, "products/created.html", {"title": "Product Created", "message": "Product created successfully!"})
        
        return render(request, self.template_name, {"title": "Create product", "form": form})
