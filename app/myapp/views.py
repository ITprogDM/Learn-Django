from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import Myapp, Category
from .forms import MyappForm, UserRegisterForm, UserLoginForm
from .utils import MyMixin


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'myapp/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, 'myapp/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')



def test(request):
    objects = ['john', 'paul', 'george', 'ringo', 'john12', 'paul23', 'george35', 'ringo41', 'salam']
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'myapp/test.html', {'page_obj': page_objects})


class HomeMyapp(MyMixin, ListView):
    model = Myapp
    template_name = 'myapp/home_myapp_list.html'
    context_object_name = 'myapp'
    mixin_prop = 'hello world'
    paginate_by = 2


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return Myapp.objects.filter(is_published=True).select_related('category')


class MyappByCategory(MyMixin, ListView):
    model = Myapp
    template_name = 'myapp/home_myapp_list.html'
    context_object_name = 'myapp'
    allow_empty = False
    paginate_by = 2

    def get_queryset(self):
        return Myapp.objects.filter(category_id=self.kwargs['category_id'],is_published=True).select_related('category')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

class ViewMyapp(DetailView):
    model = Myapp
    #pk_url_kwarg = 'myapp_id'
    #template_name = 'myapp/myapp_detail.html'
    context_object_name = 'myapp_item'



class CreateMyapp(LoginRequiredMixin, CreateView):
    form_class = MyappForm
    template_name = 'myapp/add_myapp.html'
    success_url = reverse_lazy('home')
    login_url = '/admin/'

#def index(request):
    #myapp = Myapp.objects.all()
    #context = {
        #'myapp': myapp,
        #'title': 'Список новостей',
    #}
    #return render(request, template_name='myapp/index.html', context=context)


#def get_category(request, category_id):
    #myapp = Myapp.objects.filter(category_id=category_id)
    #category = Category.objects.get(pk=category_id)

    #return render(request, template_name='myapp/category.html', context={'myapp': myapp,
    #'category' : category})
#def view_myapp(request,myapp_id):
    #myapp_item = Myapp.objects.get(pk=myapp_id)
    #myapp_item = get_object_or_404(Myapp, pk=myapp_id)
    #return render(request, 'myapp/view_myapp.html', {'myapp_item': myapp_item})


#def add_myapp(request):
    #if request.method == 'POST':
        #form = MyappForm(request.POST)
        #if form.is_valid():
            #print(form.cleaned_data)
            #myapp = Myapp.objects.create(**form.cleaned_data)
            #myapp = form.save()
            #return redirect(myapp)
    #else:
        #form = MyappForm()
    #return render(request, 'myapp/add_myapp.html', {'form': form})