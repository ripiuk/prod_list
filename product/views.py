from django.views import generic
from .models import Category, Product
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class IndexView(generic.ListView):
    template_name = 'product/index.html'
    context_object_name = 'all_categories'
    def get_queryset(self):
        return Category.objects.all()

class ProductView(generic.DetailView):
    model = Category
    template_name = 'product/product.html'
    slug_field = 'category_slug'
    slug_url_kwarg = 'category_slug'

class OneProductView(generic.DetailView):
    model = Product
    template_name = 'product/one_product.html'
    slug_field = 'product_slug'
    slug_url_kwarg = 'product_slug'

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                category = Category.objects.all()
                return render(request, 'product/index.html', {'all_categories': category})
    context = {
        "form": form,
    }
    return render(request, 'product/register.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                category = Category.objects.all()
                return render(request, 'product/index.html', {'all_categories': category})
            else:
                return render(request, 'product/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'product/login.html', {'error_message': 'Invalid login'})
    return render(request, 'product/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'product/login.html', context)

def only_tf(request):
    if not request.user.is_authenticated():
        return render(request, 'product/login.html')
    else:
        time_thereshold = datetime.now() - timedelta(hours=24)
        products = Product.objects.filter(created_at__gte = time_thereshold)
        return render(request, 'product/only_24.html', {'all_products': products})