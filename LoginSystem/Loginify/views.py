from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from .models import UserDetails
from .serializers import UserDetailsSerializer
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def print_hello(request):
    return HttpResponse("Hello World!")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, f'Email {email} already exists')
        else:
            new_user = UserDetails(username=username, email=email, password=password)
            new_user.save()
            messages.success(request, 'Signup successful! Please log in.')
            return redirect('login')
    
    return render(request, 'Loginify/signup.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
    
        try:
            existing_user = UserDetails.objects.get(email=email, password=password)
            messages.success(request, f'Welcome, {existing_user.username}')
            return render(request, "Loginify/success.html", {'user': existing_user})
        except UserDetails.DoesNotExist:
            messages.error(request, 'Invalid email or password')
    return render(request, 'Loginify/login.html')        

def get_all_users(request):
    if request.method == "GET":
        try:
            all_users = UserDetails.objects.all()
            serialized_data=UserDetailsSerializer(all_users,many=True)
            return JsonResponse(serialized_data.data, safe=False)
        except Exception as e:
            return JsonResponse({"error":str(e)})


def one_user(request, email):
    if request.method == 'GET':
        try:
            user_data=UserDetails.objects.get(email=email)
            serialized_data=UserDetailsSerializer(user_data)
            return JsonResponse(serialized_data.data, safe=False)
        except UserDetails.DoesNotExist:
            return JsonResponse({"error":"User not found"},status=404)

@csrf_exempt
def update_user(request,email):
    if request.method == 'PATCH':
        try:
            user_data=UserDetails.objects.get(email=email)
            input_data=json.loads(request.body)
            serialized_data=UserDetailsSerializer(user_data,data=input_data,partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                return JsonResponse({"message":"Data Updated Successfully"},status=200)
            else:
                return JsonResponse(serialized_data.errors,status=400)
        except UserDetails.DoesNotExist:
            return JsonResponse({"error":"User not found"},status=404)

@csrf_exempt
def delete_user(request, email):
    if request.method == 'DELETE':
        try:
            user_data=UserDetails.objects.get(email=email)
            user_data.delete()
            return JsonResponse({"message":"Data deleted successfully"},status=204)
        except UserDetails.DoesNotExist:
            return JsonResponse({"error":"User not found"},status=404)