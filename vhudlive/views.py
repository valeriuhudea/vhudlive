from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from rest_framework import status, viewsets, generics, permissions, renderers
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from .models import *
from .serializers import *
from .forms import *

### URL Page Views ###
class PageView():

    def home_page(request):
        return render(request, 'vhudlive/welcome.html')

    def delete_all_user_orders(username):
        Storage.objects.filter(owner=username).filter(already_ordered=False).delete()
        return True

    def calculate_total_price(username):
        total_prices = ''
        for obj in Storage.objects.filter(added_by=username).filter(already_ordered=False):
            price_all += obj.price
        return total_price

    def register_page(request):
        if not request.user.is_authenticated:
            if request.method == "POST":
                form = RegistrationForm(request.POST)
                if form.is_valid():
                    form.save()
                    username = form.cleaned_data["username"]
                    password = form.cleaned_data["password1"]
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect("home")
                else:
                    return("Invalid Form")
            else:
                form = RegistrationForm()
            context = {"form": form}
            return render(request, 'registration/register.html', context)
        else:
            return redirect("home")

    def login_page(request):
        if not request.user.is_authenticated:
            if request.method == "POST":
                form = AuthenticationForm(data=request.POST)
                if form.is_valid():
                    username = form.cleaned_data["username"]
                    password = form.cleaned_data["password"]
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        if next is not None:
                            return redirect("home")
                        else:
                            return redirect("home")
            else:
                form = AuthenticationForm()
            context = {"form": form}
            return render(request, 'registration/login.html', context)
        else:
            return redirect("home")

    def logout_page(request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("home")

    @login_required()
    def menu_page(request):
        form_storage = StorageForm(request.POST or None)
        form_storage_owner = request.user
        if form_storage.is_valid():
            form_storage_name = form_storage.cleaned_data["storage_name"]
            form_storage_type = form_storage.cleaned_data["storage_type"]
            #form_storage_type = StorageType.objects.get(storage_type=request.POST["storagetype"])
            #new_storage = Storage(storage_name=form_storage_name, storage_type=form_storage_type)
            new_storage.save()#storage_size=form_storage_size,
            new_storage.calculate_cart_price()
            new_storage.save()
            messages.add_message(request, messages.INFO, "Storage added!")
            form_storage = StorageForm()

        context = {}
        context.update({"Storage": Storage.objects.all()})
        #context.update({"Products": ProductType.objects.all()})
        context.update({"form_storage": form_storage})
        return render(request, 'vhudlive/menu.html', context)

    @login_required
    def cart_page(request):
        price_all = Decimal(calculate_cart_price(request.user))
        context = {}
        context.update({"price_all": price_all})
        context.update({"Storage": Storage.objects.filter(add_by=request.user).filter(already_ordered=False)})
        context.update({"Product": Products.objects.filter(add_by=request.user).filter(already_ordered=False)})

        return render(request, 'orders/cart.html', context)

    @login_required
    def user_orders_page(request):
        context = {"orders": reversed(ProperOrder.objects.filter(order_client=request.user))}
        return render(request, 'vhudlive/my_orders.html', context)

    @login_required()
    def make_order(request):
        new_proper_order = ProperOrder()
        new_proper_order.order_client = request.user
        new_proper_order.order_price = calculate_cart_price(request.user)
        new_proper_order.save()

        for item in Sub.objects.filter(add_by=request.user).filter(already_ordered=False):
            item.already_ordered = True
            item.in_order = new_proper_order
            item.save()

        for item in Storage.objects.filter(add_by=request.user).filter(already_ordered=False):
            item.already_ordered = True
            item.in_order = new_proper_order
            item.save()

        messages.add_message(request, messages.INFO, f"Order number {new_proper_order.id} send! For any questions, contact us: 0759151114")
        return redirect(user_orders_view)

    @login_required
    def clear_cart(request):
        delete_all_user_orders(request.user)
        return redirect("cart_view")

    @staff_member_required
    def all_orders_page(request):
        context = {"orders": reversed(ProperOrder.objects.all())}
        return render(request, 'vhudstorage/all_orders.html', context)

    @staff_member_required
    def mark_order_as_done(request, order_id):
        marked = VhudOrder.objects.get(id=order_id)
        marked.order_done = True
        marked.save()
        return redirect(all_orders_view)

### Api Views ###
class UsersView(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `GET` and `POST` actions for Users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupsView(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `GET` and `POST` actions for Groups.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class StorageDataView(viewsets.ModelViewSet):
    serializer_class = DataSerializer

    def get_queryset(self):
        return Data.objects.filter(data_of=self.kwargs['storage_pk'])

class StorageListView(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class StorageView(viewsets.ModelViewSet):
    #lookup_field = 'id'
    #permission_classes = [IsOwner]
    serializer_class = StorageSerializer
    queryset = Storage.objects.all()

class DataListView(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

class DataView(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

'''
class StorageListView(generics.ListCreateAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
   
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class StorageView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = StorageSerializer
    queryset = Storage.objects.all()

class DataListView(generics.ListCreateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

class DataView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = DataSerializer
    queryset = Data.objects.all()

'''
