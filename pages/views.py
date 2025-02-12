from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Product 
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from .models import Product

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
# Product Index View
# ===========================
class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products":  Product.objects.all(),
        }
        return render(request, self.template_name, viewData)


# ===========================
# Product Show View
# ===========================
from django.http import HttpResponseRedirect
from django.urls import reverse

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product ID must be 1 or greater")
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))
        product = get_object_or_404(Product, pk=product_id)

        view_data = {
            "title": f"{product.name} - Online Store",
            "subtitle": f"{product.name} - Product Information",
            "product": product
        }

        return render(request, self.template_name, view_data)

class ProductForm(forms.ModelForm):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than zero.')
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        view_data = {
            "title": "Create Product",
            "form": form
        }
        return render(request, self.template_name, view_data)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-created')
        
        view_data = {
            "title": "Create Product",
            "form": form
        }
        return render(request, self.template_name, view_data)


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
            print("Formulario válido, guardando en la base de datos...")
            form.save()
            return redirect('product-created')  

        print(" Errores en el formulario:", form.errors) 

        view_data = {
        "title": "Create Product",
        "form": form
    }
        return render(request, self.template_name, view_data)

    


# ===========================
# Product list View
# ===========================
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products' 

    def get_context_data(self, **kwargs):
        # Obtener el contexto base de la clase padre
        context = super().get_context_data(**kwargs)

        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of Products'
        
        return context
    

class ProductCreatedView(TemplateView):
    template_name = "products/created.html"
