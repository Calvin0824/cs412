from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import random
import datetime


SPECIAL = [("Marinated Duck", 37), ("Soy Sauce Chicken", 29), ("Poached Chicken", 29), ("BBQ Pork", 19), ("Marinated Beef Tripe", 18), ("Chinese Broccoli", 15), ("Ice Berg Lettuce", 15)]

# Create your views here.
def main(request):
    """the main page where it will display the restuarant"""
    img = "/static/images/HongKongEatery.jpg"
    context = {"img":img}
    return render(request, 'restaurant/main.html', context)

def order(request):
    """the order page where it will display the menu"""
    today = random.choice(SPECIAL)
    context = {"today": today[0], "price": today[1]}
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    """the confirmation page where it will display the order"""
    if request.POST:
        order = request.POST.getlist("order")
        today = request.POST.get("today")
        instructions = request.POST.get("instructions")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        total = 0
        order_list = []
        mod_list = []
        for i in order:
            item, price = i.split(";")
            total += int(price)
            order_list.append(item)

            if i == "House Fried Rice;15":
                mod = request.POST.getlist("modifications")
                for m in mod:
                    item, price = m.split(";")
                    total += int(price)
                    mod_list.append(item)
        if today:
            special, p = today.split(";")
            total += int(p)

        current_time = datetime.datetime.now()
        rand = random.randint(30, 60)
        ready_time = current_time + datetime.timedelta(minutes=rand)
        
        context = {"order": order_list, 
                   "modifications": mod_list,
                   "today": special,
                   "ready_time": ready_time,
                   "instructions": instructions,
                   "total": total,
                   "name": name,
                   "phone": phone,
                   "email": email}
        return render(request, 'restaurant/confirmation.html', context)

    return redirect('main')