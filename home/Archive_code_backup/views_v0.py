from django.shortcuts import render,redirect
# from home.models import Contact
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
import requests
import json
import os
import base64
from django.http import JsonResponse
import openai 
openai.api_key = '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'


def home(request):  
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def projects(request): # 4) the request then comes here 
    if request.method == 'POST':
        username = request.POST['username'] #the user enters the username in the ui , the entered ui , these values come from projects.html template
        password = request.POST['password'] #the user enters the password in the ui , the entered ui , these values come from projects.html template
        # regarding the above , u can have look at the projects.html file in templates folder
        valid_credentials = {
            'sai.sumanthkakkirala@iqvia.com': 'sai@123',
            'karuna.tirumala@iqvia.com': 'karuna@123',
            'karthik.s3@iqvia.com': 'karthik@123',
        }
        #5 ) the script checks if the details entered by the user are in the valid_credentials dictionary 
        if username in valid_credentials and password == valid_credentials[username]: 
            # Store the username in session to remember the logged-in user
            request.session['username'] = username
            return redirect('home')  # 6) if yes ,Redirect to home page after successful login
        else:
            error_message = 'Username or password entered is incorrect.'
            return render(request, 'projects.html', {'error_message': error_message})
    #7 ) if the creds are not in the dictionary , the script will not direct him to home page, he will remain in same page
    return render(request, 'projects.html') #3) the user will see the project.html page 



def contacts(request):
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']
        print(name ,email, phone, desc)
        contact = Contact(name=name, email= email, phone=phone , desc=desc)
        contact.save()
        print("the data has been returened to the DB") 
    return render(request, 'contacts.html')
# def ask_openai(message):
#     response = openai.ChatCompletion.create(
#         model = "text-davinci-003",
#         prompt = message,
#         max_tokens = 150,
#         n=1,
#         stop = None,
#         temperature = 0.7,
#     )
#     print(response)    
#     answer = response.choice[0].text.strip()
#     return answer
def ask_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ]
        )
    
       
    answer = response.choices[0].message.content
    return answer

def workbench(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
#         response = f"""Sure!. DCX123 is of doctor Karuna, who works in location Bangalore. Below are the sync details.
# MDM: \n
# ID: DCX123 \n
# Name: Karuna\n
# Affiliates to : Clinic1\n
# Work location : Bangalore\n
# Specialty : General Physician\n
# OCEP:\n
# ID : OCEP123\n
# City: Bangalore\n
# """
        print(response)
        return JsonResponse({'message': message, 'response': response})
    
    return render(request, 'workbench.html')