from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation
# from home.models import FAQ
from order.models import Order, OrderProduct
from product.models import Category, Comment
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.


@login_required(login_url='/login')  # Check login
def index(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category, 'profile': profile}
    return render(request, 'pages/user_profile.html', context)


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            # *** Multi Langugae
            # request.session[translation.LANGUAGE_SESSION_KEY] = userprofile.language.code
            # request.session['currency'] = userprofile.currency.code
            # translation.activate(userprofile.language.code)

            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(
                request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.

    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'pages/login_form.html', context)
    # return JsonResponse({"done": 'sweet'})


def logout_func(request):
    logout(request)
    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]
        del request.session['currency']
    return HttpResponseRedirect('/')


def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
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

    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'pages/signup_form.html', context)


@login_required(login_url='/login')  # Check login
def user_update(request):
    if request.method == 'POST':
        # request.user is user  data
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        # "userprofile" model -> OneToOneField relatinon with user
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'pages/user_update.html', context)


@login_required(login_url='/login')  # Check login
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,
                             'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(
                request,
                'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'pages/change_password.html', {
            'form': form,
            'category': category
        })


@login_required(login_url='/login')  # Check login
def my_orders(request):
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user__id=current_user.id)
    context = {
        'category': category,
        'orders': orders,
    }
    return render(request, 'pages/user_orders.html', context)


@login_required(login_url='/login')  # Check login
def order_detail(request, id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'pages/order_detail.html', context)


@login_required(login_url='/login')  # Check login
def my_comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'pages/my_comments.html', context)


@login_required(login_url='/login')  # Check login
def user_deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')