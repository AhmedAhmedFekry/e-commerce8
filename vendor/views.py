from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404
from vendor.models import Vendor
from product.models import Category
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from product.models import Category, Product
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile
from vendor.form import ProductForm


def become_vendor(request):
    category = Category.objects.all()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create vendor
            vendor = Vendor.objects.create(name=user.username, created_by=user)
            # Create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')
    else:
        form = SignUpForm()
        return render(request, 'vendor/become_vendor.html', {
            'form': form,
            "category": category,
            'request': request
        })


def login_vendor(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        try:
            vendor = get_object_or_404(Vendor, name=user.username)
            if vendor.status == False:
                raise Exception
            # vendor = Vendor.objects.get(name=user.username, status=True)
        except:
            messages.warning(request, "the vendor is not exists ")
            return HttpResponseRedirect('/')
        # if user.vendor.filter(status=True):
        #     pass
        # else:
        #     messages.warning(request, "the vendor is not exists 64")
        #     return HttpResponseRedirect('/')

        if user:
            login(request, user)
            request.session['currency'] = 'EGP'
            messages.success(request, "the vendor is exists")

            return redirect('vendor_admin')
        else:
            messages.warning(request, "the vendor is not exists ")
            return HttpResponseRedirect('/')

    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'pages/login_form.html', context)


@login_required
def vendor_admin(request):
    category = Category.objects.all()
    vendor = request.user.vendor
    products = vendor.products.all()

    return render(request, 'vendor/vendor_admin.html', {
        'vendor': vendor,
        'category': category,
        'products': products,
    })


@login_required
def add_product(request):
    category = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.title = product.title_en
            product.description = product.description_en
            product.slug_en = slugify(product.title_en, allow_unicode=True)
            product.slug_ar = slugify(product.title_ar, allow_unicode=True)
            product.slug = slugify(product.title_en, allow_unicode=True)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()

    return render(request, 'vendor/add_product.html', {
        'form': form,
        'category': category
    })


def edit_product(request, product_id):
    # ve
    # product = get_object_or_404(Product, id=product_id)
    vendor = get_object_or_404(Vendor, created_by=request.user)
    try:
        product = vendor.products.get(id=product_id)
    except:
        return HttpResponse('this product no belongs to your')
    # product = Product.objects.filter(id=product_id, vendor=vendor)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        print('line done            129')
        if form.is_valid():
            print('line done            131')
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.title = product.title_en
            product.description = product.description_en
            product.slug_en = slugify(product.title_en, allow_unicode=True)
            product.slug_ar = slugify(product.title_ar, allow_unicode=True)
            product.slug = slugify(product.title_en, allow_unicode=True)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm(instance=product)

    return render(request, 'vendor/edit_product.html', {
        'form': form,
    })