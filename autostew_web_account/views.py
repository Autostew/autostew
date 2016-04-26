from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404

from autostew_web_session.models.models import SetupRotationEntry, SetupQueueEntry
from autostew_web_session.models.server import Server
from autostew_web_session.models.session import SessionSetup
from autostew_web_users.models import SafetyClass


def register_view(request):
    if request.user.is_authenticated():
        return redirect('account:home')
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, "An account with this email address already exists", extra_tags="error")
            return redirect('account:register')

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, "An account with this username already exists", extra_tags="error")
            return redirect('account:register')

        if password != password2:
            messages.add_message(request, messages.ERROR, "Your passwords don't match!", extra_tags="error")
            return redirect('account:register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.add_message(request, messages.SUCCESS, "Account created. Please log in.", extra_tags="success")
        return redirect('account:login')

    else:
        return render(request, 'autostew_web_account/register.html')


def login_view(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Login successful.", extra_tags='success')
                return redirect('account:home')
            else:
                messages.add_message(request, messages.ERROR, "You account is disabled.", extra_tags='danger')
                return redirect('account:login')
        else:
            messages.add_message(request, messages.ERROR, "Your username and/or your password is incorrect.", extra_tags='warning')
            return redirect('account:login')
    else:
        if request.user.is_authenticated():
            return redirect('account:home')
        else:
            return render(request, 'autostew_web_account/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "You have been logged out.", extra_tags='success')
    return redirect('home:home')


@login_required
def account_view(request):
    context = {
        'servers': Server.objects.filter(owner=request.user),
        'safety_classes': SafetyClass.objects.all(),
    }
    return render(request, 'autostew_web_account/home.html', context)


@login_required
def add_view(request):
    if request.POST:
        Server.objects.create(
            name=request.POST.get('name'),
            api_username=request.POST.get('api_username'),
            api_password=request.POST.get('api_password'),
            api_address=request.POST.get('api_address'),
            api_port=request.POST.get('api_port'),
            owner=request.user,
            max_member_count=32,
        )
        messages.add_message(
            request,
            messages.SUCCESS,
            "Your DS has been registered. It will be manually verified and activated, so please be patient as this may take some times (from hours up to some days if we are currently too busy).",
            extra_tags='success'
        )
        return redirect('account:home')
    else:
        return render(request, 'autostew_web_account/add_server.html')


@login_required
def settings_view(request, pk):
    server = get_object_or_404(Server, pk=pk)
    context = {'server': server}
    return render(request, 'autostew_web_account/server_settings.html', context)


@login_required
def rotation_view(request, pk):
    server = get_object_or_404(Server, pk=pk)
    context = {'server': server, 'setup_templates': SessionSetup.objects.filter(is_template=True)}
    return render(request, 'autostew_web_account/setup_rotation.html', context)


@login_required
def queue_view(request, pk):
    server = get_object_or_404(Server, pk=pk)
    context = {'server': server, 'setup_templates': SessionSetup.objects.filter(is_template=True)}
    return render(request, 'autostew_web_account/setup_queue.html', context)


@login_required
def remove_rotated_setup(request, server_pk, entry_pk):
    server = get_object_or_404(Server, pk=server_pk, owner=request.user)
    entry = get_object_or_404(SetupRotationEntry, pk=entry_pk, server=server)
    entry.delete()
    messages.add_message(request, messages.SUCCESS, "The setup has been removed from the rotation.", extra_tags='success')
    return redirect('account:rotation', pk=server.id)


@login_required
def add_setup_to_rotation(request, server_pk, setup_pk):
    server = get_object_or_404(Server, pk=server_pk, owner=request.user)
    setup = get_object_or_404(SessionSetup, pk=setup_pk, is_template=True)
    SetupRotationEntry.objects.create(
        order=len(SetupRotationEntry.objects.filter(server=server)),
        setup=setup,
        server=server,
    )
    messages.add_message(request, messages.SUCCESS, "The setup has been added to the rotation.", extra_tags='success')
    return redirect('account:rotation', pk=server.id)


@login_required
def remove_queued_setup(request, server_pk, entry_pk):
    server = get_object_or_404(Server, pk=server_pk, owner=request.user)
    entry = get_object_or_404(SetupQueueEntry, pk=entry_pk, server=server)
    entry.delete()
    messages.add_message(request, messages.SUCCESS, "The setup has been removed from the queue.", extra_tags='success')
    return redirect('account:queue', pk=server.id)


@login_required
def add_setup_to_queue(request, server_pk, setup_pk):
    server = get_object_or_404(Server, pk=server_pk, owner=request.user)
    setup = get_object_or_404(SessionSetup, pk=setup_pk, is_template=True)
    SetupQueueEntry.objects.create(
        order=len(SetupQueueEntry.objects.filter(server=server)),
        setup=setup,
        server=server,
    )
    messages.add_message(request, messages.SUCCESS, "The setup has been added to the queue.", extra_tags='success')
    return redirect('account:queue', pk=server.id)
