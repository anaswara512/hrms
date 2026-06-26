from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

User = get_user_model()


def login_view(request):

    if request.method=="POST":

        username=request.POST.get("username")

        password=request.POST.get("password")

        user=authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request,user)

            if user.role=="ADMIN":

                return redirect("/dashboard/admin/")

            elif user.role=="HR":

                return redirect("/dashboard/")

            else:

                return redirect("/dashboard/employee/")

        return render(
            request,
            "accounts/login.html",
            {
                "error":"Invalid Username or Password"
            }
        )

    return render(
        request,
        "accounts/login.html"
    )


from django.utils import timezone
from employees.models import Employee

@login_required
def register_view(request):
    if request.user.role not in ["ADMIN", "HR"]:
        raise PermissionDenied("You are not authorized to onboard new employees.")

    if request.method == "POST":
        full_name = request.POST.get("full_name", "")
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        role = request.POST.get("role", "EMPLOYEE")
        phone = request.POST.get("phone", "")
        department = request.POST.get("department", "")

        # Validation
        if password != confirm_password:
            return render(request, "accounts/register.html", {"error": "Passwords do not match."})

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {"error": "Username already exists."})

        if User.objects.filter(email=email).exists():
            return render(request, "accounts/register.html", {"error": "Email already exists."})

        # Split full name
        first_name, last_name = "", ""
        if full_name:
            parts = full_name.split(" ", 1)
            first_name = parts[0]
            if len(parts) > 1:
                last_name = parts[1]

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            first_name=first_name,
            last_name=last_name
        )

        # Auto-create Employee profile for all roles (Employee, HR, Admin)
        employee_id = f"EMP{user.id:04d}"
        if role == 'HR':
            designation = "HR Manager"
            default_dept = "Human Resource"
        elif role == 'ADMIN':
            designation = "System Admin"
            default_dept = "Administration"
        else:
            designation = "Trainee"
            default_dept = "General"

        Employee.objects.create(
            user=user,
            employee_id=employee_id,
            phone=phone,
            department=department if department else default_dept,
            designation=designation,
            joining_date=timezone.now().date(),
            salary=0.00
        )

        messages.success(request, f"User account '{username}' ({role.lower()}) created successfully.")
        return redirect("employee_list")

    return render(
        request,
        "accounts/register.html"
    )



def logout_view(request):

    logout(request)

    return redirect("/")