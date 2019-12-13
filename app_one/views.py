from django.shortcuts import render, redirect
from app_one.models import *
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import bcrypt

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):

    if User.objects.is_reg_valid(request) is False:
        # redirect back to same page they came from to display errors
        return redirect('/')

    hashed_pw = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed_pw,
    )

    request.session['uid'] = new_user.id
    return redirect('/wishes')


def login(request):
    found_users = User.objects.filter(email=request.POST['email'])

    if len(found_users) < 1:
        messages.error(request, 'Invalid Credentials')
        return redirect('/')
    else:
        user_from_db = found_users[0]

        is_pw_correct = bcrypt.checkpw(
            request.POST['password'].encode(), user_from_db.password.encode())

        if is_pw_correct is True:
            request.session['uid'] = user_from_db.id
            return redirect('/wishes')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')

# *******************************


def wishes_page(request):

    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    logged_in_user = User.objects.get(id=uid)

    context = {
        'current_user': User.objects.get(id=uid),
        'all_wishes_by_logged_in_user': User.objects.get(id=uid).wishes.all(),
        'ungranted_wishes': Wish.objects.filter(is_granted=False),
        'granted_wishes': Wish.objects.filter(is_granted=True),
        'all_wishes': Wish.objects.all(),
        'logged_in_user': logged_in_user,
    }

    return render(request, 'wish_dashboard.html', context)


def like(request, wish_id):
    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    logged_in_user = User.objects.get(id=uid)

    found_wish = Wish.objects.filter(id=wish_id)

    if len(found_wish) > 0:
        wish_to_like = found_wish[0]

        if logged_in_user in wish_to_like.likes.all():
            wish_to_like.likes.remove(logged_in_user)
        else:
            wish_to_like.likes.add(logged_in_user)

    return redirect('/wishes')


def new_wish_page(request):

    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    context = {

        'logged_in_user': User.objects.get(id=uid),

    }

    return render(request, 'new_wish_page.html', context)


def create_wish(request):

    if Wish.objects.is_form_valid(request) is False:
            # redirect back to same page they came from to display errors
        return redirect('/wishes/new')

    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    logged_in_user = User.objects.get(id=uid)

    new_wish = Wish.objects.create(
        item_name=request.POST['item_name'], description=request.POST['description'], wished_by=logged_in_user)

    return redirect('/wishes')


def remove(request, wish_id):

    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    logged_in_user = User.objects.get(id=uid)

    found_wish = Wish.objects.filter(id=wish_id)

    if len(found_wish) > 0:
        wish_to_delete = found_wish[0]

        if logged_in_user == wish_to_delete.wished_by:
            wish_to_delete.delete()

    return redirect('/wishes')


def edit_page(request, wish_id):

    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    context = {
        'current_wish': Wish.objects.get(id=wish_id),
        'logged_in_user': User.objects.get(id=uid),
        'wish': Wish.objects.get(id=wish_id),
    }

    return render(request, 'edit_wish_page.html', context)


def edit(request, current_wish_id):
    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    if Wish.objects.is_form_valid(request) is False:
            # redirect back to same page they came from to display errors
        return redirect(f'/wishes/edit/{current_wish_id}')

    found_wish = Wish.objects.filter(id=current_wish_id)

    if len(found_wish) > 0:
        logged_in_user = User.objects.get(id=uid)
        wish_to_update = found_wish[0]

        if logged_in_user != wish_to_update.wished_by:
            return redirect('/wishes')

        wish_to_update.item_name = request.POST['item_name']
        wish_to_update.description = request.POST['description']
        wish_to_update.save()
        return redirect('/wishes')

    else:
        return redirect('/wishes')


def grant_wish(request, wish_id):

    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    found_wish = Wish.objects.filter(id=wish_id)

    if len(found_wish) != 0:
        wish = found_wish[0]
        wish.is_granted = not wish.is_granted
        wish.save()
    return redirect('/wishes')


def stat_page(request):

    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    is_wish_granted = Wish.objects.all()

    context = {
        'current_user': User.objects.get(id=uid),
        'all_wishes_by_logged_in_user': User.objects.get(id=uid).wishes.all(),
        'ungranted_wishes': Wish.objects.filter(is_granted=False),
        'granted_wishes': Wish.objects.filter(is_granted=True),
        'current_user_granted_wishes': User.objects.get(id=uid).wishes.filter(is_granted=True),
        'current_user_ungranted_wishes': User.objects.get(id=uid).wishes.filter(is_granted=False),
    }

    return render(request, 'stat_page.html', context)
