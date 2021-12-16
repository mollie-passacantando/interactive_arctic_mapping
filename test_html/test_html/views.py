from django.shortcuts import render


import requests
data = requests.get('https://regres.in/api/users;')

print(data.text)


def button(request):
    return render(request,'home.html')


def output(request):
    import requests
    data = requests.get('https://regres.in/api/users')
    print(data.text)
    data = data.text
    return render(request,'home.html',{'data':data})

