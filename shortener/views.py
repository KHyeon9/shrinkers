# from django.http import JsonResponse
# from django.shortcuts import render, redirect
# from shortener.forms import LoginForm, RegisterForm
# from shortener.models import Users
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth import login, authenticate, logout
# from django.core.paginator import Paginator
# from django.contrib.auth.decorators import login_required

# # Create your views here.


# def index(request):
#     return render(request, "base.html")


# @csrf_exempt
# def get_user(request, user_id):
#     print(user_id)
#     if request.method == "GET":
#         abc = request.GET.get("abc")
#         xyz = request.GET.get("xyz")
#         user = Users.objects.filter(pk=user_id).first()
#         return render(request, "base.html", {"user": user, "params": [abc, xyz]})
#     elif request.method == "POST":
#         username = request.GET.get("username")

#         if username:
#             user = Users.objects.filter(pk=user_id).update(username=username)

#     return JsonResponse(status=201, data=dict(msg="You just reached with Post Method!", safe=False))


# def register(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         msg = "올바르지 않은 데이터입니다."

#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             raw_password = form.cleaned_data.get("password1")
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             msg = "회원가입 완료"

#         context = {'form': form,  "msg": msg}
#         return render(request, "register.html", context)

#     else:
#         form = RegisterForm()
#         context = {'form': form}
#         return render(request, "register.html", context)


# def login_view(request):
#     is_ok = False
#     if request.method == "POST":
#         form = LoginForm(request.POST)

#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             raw_password = form.cleaned_data.get("password")
#             remember_me = form.cleaned_data.get("remember_me")
#             msg = "올바른 유저ID와 패스워드를 입력하세요."

#             try:
#                 user = Users.objects.get(user__email=email)

#             except Users.DoesNotExist:
#                 pass

#             else:
#                 if user.user.check_password(raw_password):
#                     msg = None
#                     login(request, user.user)
#                     is_ok = True
#                     request.session["remember_me"] = remember_me

#     else:
#         msg = None
#         form = LoginForm()

#     print("REMEMBER_ME: ", request.session.get("remember_me"))

#     context = {"form": form, "msg": msg, "is_ok": is_ok}
#     return render(request, "login.html", context)


# def logout_view(request):
#     logout(request)
#     return redirect("login")


# @login_required
# def list_view(request):
#     page = int(request.GET.get("p", 1))
#     users = Users.objects.all().order_by("-id")
#     paginator = Paginator(users, 10)
#     users = paginator.get_page(page)

#     context = {"users": users}
#     return render(request, "boards.html", context)
