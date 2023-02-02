from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import FormView
from django.views.generic import UpdateView, ListView, TemplateView
from apps.accounts.models import User
from django.contrib.auth.models import  Permission
from django.contrib.auth.decorators import login_required, permission_required

from apps.inventory.models import Brand, Category, Product, WareHouse
from apps.order.models import OrderIn, OrderOut
from .froms import UserCreationForm, UserEditForm, UserAddForm , UserRegistrationForm, ChangePasswordForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
import logging
from django.contrib.admin.views.main import ChangeList
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.utils.translation import gettext as _

# Create your views here.
# logger = logging.getLogger(__name__)
class SignupView(FormView):
    template_name = "accounts/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:signup_success')
    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        return response    

class SignupsuccessView(TemplateView):
    template_name = "accounts/signup_message.html" 


class UserView(TemplateView):
    model = User
    template_name= "accounts/user-detail.html"
  

class UserUpdateView(UpdateView):
    model = User
    form_class= UserEditForm
    template_name = 'accounts/edit-user.html' 
    success_url = reverse_lazy('accounts:userdetail')

class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'accounts.view_user'

    template_name = 'accounts/user_list.html' 
    success_url = reverse_lazy('accounts:userlist')
    context_object_name= "users"
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context["warehouses"] = WareHouse.objects.all()
        context["permissions"] = Permission.objects.all()
        content_type = ContentType.objects.get_for_model(Product)
        post_permission = Permission.objects.filter(content_type=content_type)
        context["post_permission"] = Permission.objects.filter(content_type=content_type)

        print([perm.codename for perm in post_permission])
        return context 


class UserAddView(PermissionRequiredMixin, FormView):
    template_name = "accounts/snippets/create_user.html"
    permission_required = 'accounts.add_user'

    form_class = UserAddForm
    success_url = reverse_lazy('accounts:userlist')
    def get_context_data(self, **kwargs):
        context = super(UserAddView, self).get_context_data(**kwargs)
        print("hello" )
        context["warehouses"] = WareHouse.objects.all()
        context["permissions"] = Permission.objects.all()
        # context["user_permissions"] = Permission.objects.filter(self.perm)
        return context 

class UserChangeView(PermissionRequiredMixin, UpdateView):
    model = User
    permission_required = 'accounts.change_user'

    form_class= UserAddForm
    template_name = 'accounts/snippets/change_user.html' 
    success_url = reverse_lazy('accounts:userlist')
    def get_context_data(self, **kwargs):
        context = super(UserChangeView, self).get_context_data(**kwargs)
        context["warehouses"] = WareHouse.objects.all()
        context["permissions"] = Permission.objects.all()
        content_type_product = ContentType.objects.get_for_model(Product)
        content_type_category = ContentType.objects.get_for_model(Category)
        content_type_brand = ContentType.objects.get_for_model(Brand)
        content_type_warehouse = ContentType.objects.get_for_model(WareHouse)
        content_type_orderin = ContentType.objects.get_for_model(OrderIn)
        content_type_orderout = ContentType.objects.get_for_model(OrderOut)
        content_type_user = ContentType.objects.get_for_model(User)
        context["post_permission_product"] = Permission.objects.filter(content_type=content_type_product)
        context["post_permission_category"] = Permission.objects.filter(content_type=content_type_category)
        context["post_permission_brand"] = Permission.objects.filter(content_type=content_type_brand)
        context["post_permission_warehouse"] = Permission.objects.filter(content_type=content_type_warehouse)
        context["post_permission_orderin"] = Permission.objects.filter(content_type=content_type_orderin)
        context["post_permission_orderout"] = Permission.objects.filter(content_type=content_type_orderout)
        context["post_permission_user"] = Permission.objects.filter(content_type=content_type_user)

        return context

    def form_valid(self,  form):
        perms = self.request.POST.getlist('perms')
        user_pk = self.request.POST.get('my_user')
        user =  get_object_or_404(User, id=user_pk)
        user.user_permissions.set(perms)
        user.save()
        print('YESSS')

        print('formset not valid==========', form.errors)
        return super().form_valid( form)
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Error: formulaire non valid," f'{form.errors}')
        print("THE ERRORS in INVALID_FORM======: ", form.errors)
        return redirect('accounts:userlist')
        

def add_user(request):
    context= {}
    if request.method == 'POST' :
        print('ouiii regiuster')
        user_form = UserRegistrationForm(request.POST)
        context['user_form'] = user_form,
        if user_form.is_valid():
            cd = user_form.cleaned_data
            email = cd['email']
            password = cd['password']
            password2 = cd['password2']
            print('user form valid')

            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(request,_('un utilisateur avec cet email éxiste déja'))
                    print('"yeaaah lha9t hnadeeeeertrrr')
                    return redirect('accounts:userlist')
                    
                print('"yeaaah lha9t hna')
            else:
                messages.error(request, _('les mots de passes ne sont pas identique') )
                return redirect('accounts:userlist')
            new_user = User.objects.create_user(
                # phone=cd['phone'],
                # address=cd['address'],
                email=email,
                role=" ",
                password=password
            )
            context['new_user'] = new_user
            return redirect('accounts:userlist')
        else:
            messages.error(request, user_form.errors)
            print('erruers ', user_form.errors)

            context['user_form'] = UserRegistrationForm()

    else:
        context['user_form'] = UserRegistrationForm()
        return redirect('accounts:userlist')

    # return render(request,'register.html' ,context)
@permission_required('accounts.change_user', raise_exception=True)
def change_password(request, pk):
    context= {}
    if request.method == 'POST' :
        user = get_object_or_404(User , pk=pk)
        user_form = ChangePasswordForm(request.POST)
        context['change_password_form'] = user_form
        if user_form.is_valid():
            cd = user_form.cleaned_data
            # email = cd['email']
            password = cd['password']
            password2 = cd['password2']
            print('user form valid')
            # user = get_object_or_404(User, email=email)
            if password == password2:
                user.set_password(password)
                messages.success(request,_('Mot de passe modifié avec succés'))
                print('OOOOOOOOOOO')
                user.save()
                return redirect('accounts:userlist')
            else:
                messages.error(request, _('les mots de passes ne sont pas identique') )
                return redirect('accounts:userlist')
        else:
            messages.error(request, user_form.errors)
            print('erruers ', user_form.errors)
            print('email----> ', user_form.cleaned_data['email'])
            context['change_password_form'] = ChangePasswordForm()
    return redirect('accounts:userlist')

