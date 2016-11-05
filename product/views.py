from django.views import generic
from .models import Category, Product
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .forms import UserForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(generic.ListView):
    template_name = 'product/index.html'
    context_object_name = 'all_categories'
    def get_queryset(self):
        return Category.objects.all()

class ProductView(generic.ListView):
    template_name = 'product/product.html'
    context_object_name = 'the_product'

    def get_queryset(self, *args, **kwargs):
        c = Category.objects.filter(category_slug=self.kwargs['category_slug'])
        return Product.objects.filter(category = c)

class OneProductView(generic.DetailView):
    model = Product
    template_name = 'product/one_product.html'
    slug_field = 'product_slug'
    slug_url_kwarg = 'product_slug'

class RegisterView(generic.FormView):
    template_name = 'product/register.html'
    form_class = UserForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form =self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('product:index')
            return render(request, self.template_name, {'form': form})

class LoginView(generic.FormView):
    template_name = 'product/login.html'
    form_class = AuthenticationForm

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('product:index'))
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(reverse('product:login_user'))

class LogoutView(generic.RedirectView):
    url = '/products'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

class Only_TF(LoginRequiredMixin,generic.ListView):
    template_name = 'product/only_24.html'
    context_object_name = 'only_24_products'
    login_url = '/products/login_user/'

    def get_queryset(self):
        time_thereshold = datetime.now() - timedelta(hours=24)
        return Product.objects.filter(created_at__gte = time_thereshold)
