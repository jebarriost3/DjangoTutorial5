from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from django import forms
from .models import Product
from .utils import ImageLocalStorage


def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'images/index.html'

        def get(self, request):
            image_url = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('image_index')

    return ImageView

class ImageViewNoDI(View):
    template_name = 'images/index.html'

    def get(self, request):
        image_url = request.session.get('image_url', '')
        return render(request, self.template_name, {'image_url': image_url})

    def post(self, request):
        image_storage = ImageLocalStorage()
        image_url = image_storage.store(request)

        if image_url:
            request.session['image_url'] = image_url
        
        return redirect('image_index')

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




# ===========================
# Cart View
# ===========================
class CartView(View):
    template_name = 'cart/index.html'

    def get(self, request):
        products = {
            121: {'name': 'Tv Samsung', 'price': '1000'},
            11: {'name': 'iPhone', 'price': '2000'}
        }
        cart_products = {}
        cart_product_data = request.session.get('cart_product_data', {})

        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product
        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products
        }

        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        cart_product_data = request.session.get('cart_product_data', {})
        cart_product_data[product_id] = product_id
        request.session['cart_product_data'] = cart_product_data

        return redirect('cart_index')


# ===========================
# Cart Remove All View
# ===========================
class CartRemoveAllView(View):
    def post(self, request):
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']
        
        return redirect('cart_index')
