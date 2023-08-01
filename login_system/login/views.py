from django.shortcuts import render,redirect
from django.views import View
from login.models import*
from django.contrib import messages


# ================================== User Registration Page ==================================
class User_Registraion(View):
    def get(self, request):
        return render(request, "registration.html")

    def post(self, request):
        if request.method == "POST":
            first_name = request.POST.get("firstname")
            last_name = request.POST.get("lastname")
            email = request.POST.get("email")
            username = request.POST.get("username")
            password = request.POST.get("password")
            confirm_password = request.POST.get("cpassword")
            agree = request.POST.get("agree")
            profile_pic = request.FILES.get("pic")

            value = {
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "email": email,
            }

            error_message = None
            user = UserProfile(
                first_name=first_name,
                last_name=last_name,
                email=email,
                profile_pic=profile_pic,
                username=username,
                password=password,
            )
            if not first_name:
                error_message = "First Name is Required !!"
            elif not last_name:
                error_message = "Last Name is Required !!"
            elif not username:
                error_message = "Username is Required !!"
            elif not email:
                error_message = "Email is Required !!"
            elif not password:
                error_message = "Password is Required !!"
            elif not confirm_password:
                error_message = "Confirm Password is Required !!"
            elif not password == confirm_password:
                error_message = "Password & Confirm Password Should be Same !!"
            elif user.isExists():
                error_message = "Username Already Exists !!"
            elif not agree:
                error_message = "Please Select Our Terms & Condition !!"
            if not error_message:
                user.save()
                messages.success(request,"Account Created Successfully")
                return redirect("user_login")
            else:
                data = {
                    "error": error_message,
                    "value": value,
                }
                return render(request, "registration.html", data)


# ===========================================================================================




# =================================== Login Page =============================================
class User_Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        pass


# ===========================================================================================
