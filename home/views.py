from django.shortcuts import render,redirect
# from home.models import Contact
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
import requests
import json
import os
import base64
from django.http import JsonResponse , HttpResponseBadRequest
from django.template.defaultfilters import linebreaksbr
from .SmartSyncBot_UI_V2 import *





def home(request):  
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
def Faq(request):
    return render(request ,'Faq.html')
def Help(request):
    return render(request, 'help.html')


def projects(request): # 4) the request then comes here 
    if request.method == 'POST':
        username = request.POST['username'] #the user enters the username in the ui , the entered ui , these values come from projects.html template
        password = request.POST['password'] #the user enters the password in the ui , the entered ui , these values come from projects.html template
        # regarding the above , u can have look at the projects.html file in templates folder
        valid_credentials = {
            'sai.sumanthkakkirala@iqvia.com': 'sai@123',
            'karuna.tirumala@iqvia.com': 'karuna@123',
            
            
        }
        #5 ) the script checks if the details entered by the user are in the valid_credentials dictionary 
        if username in valid_credentials and password == valid_credentials[username]: 
            # Store the username in session to remember the logged-in user
            request.session['username'] = username
            return redirect('workbench')  # 6) if yes ,Redirect to home page after successful login
        else:
            error_message = 'OOPS!! Seems like Username or password entered is incorrect,Please Try again.'
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


def workbench(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = smartsyncbot(message)


        print("\nWorkbench Respose\n",response)
        x=JsonResponse({'message': message, 'response': response})
        print("\n X as byte \n",x.content,"\n")
        print("\n X as String \n",x.content.decode('utf-8'))
        
        
        
        # Convert newline characters to HTML line breaks
        #response_with_linebreaks = linebreaksbr(response)
        
        #response_repl=response.replace("\n","<br>")
        
        if "!DOCTYPE" in response :
            response_frmt=response
        else :
            response_frmt=linebreaksbr(response)

        
        y=JsonResponse({'message': message, 'response': response_frmt})
        print("\n Y as byte \n",y.content,"\n")
        print("\n Y as String \n",y.content.decode('utf-8'))
        
        
        return JsonResponse({'message': message, 'response': response_frmt})
    
    return render(request, 'workbench.html')