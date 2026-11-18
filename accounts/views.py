from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .decorators import role_required
from .forms import ProfileForm, RegisterForm
from .models import User


def home(request):
    if request.user.is_authenticated:
        return redirect(request.user.dashboard_url_name)
    return render(request, "accounts/home.html")


def register(request):
    if request.user.is_authenticated:
        return redirect(request.user.dashboard_url_name)
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. Welcome to GapGo!")
            return redirect(user.dashboard_url_name)
        messages.error(request, "Please fix the errors below.")
    return render(request, "accounts/register.html", {"form": form})


class GapGoLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        from django.urls import reverse
        return self.get_redirect_url() or reverse(self.request.user.dashboard_url_name)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome back, {form.get_user().first_name or form.get_user().username}!")
        return response


@require_POST
def logout_view(request):
    from django.contrib.auth import logout

    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("accounts:login")


@login_required
def dashboard(request):
    """Sends each user to the dashboard for their role."""
    return redirect(request.user.dashboard_url_name)


@role_required(User.Role.STUDENT)
def student_dashboard(request):
    return render(request, "accounts/student_dashboard.html")


@role_required(User.Role.ADMIN)
def admin_dashboard(request):
    context = {
        "student_count": User.objects.filter(role=User.Role.STUDENT).count(),
        "admin_count": User.objects.filter(role=User.Role.ADMIN).count(),
        "recent_students": User.objects.filter(role=User.Role.STUDENT).order_by("-date_joined")[:5],
    }
    return render(request, "accounts/admin_dashboard.html", context)


@login_required
def profile(request):
    # Always the logged-in user's own profile; no user id in the URL.
    return render(request, "accounts/profile.html")


@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
        messages.error(request, "Please fix the errors below.")
    return render(request, "accounts/profile_edit.html", {"form": form})
