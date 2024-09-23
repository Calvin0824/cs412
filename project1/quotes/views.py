from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

QUOTES = ["I'm crazy, but I'm not stupid.", 
          "If there really is a god, then he really looks after me.", 
          "If you're too free, you're like the way Hong Kong is now. It's very chaotic."]
PICS = ["/static/images/chan.jpeg",
        "/static/images/Jackie.jpeg",
        "/static/images/jackiechan.jpeg"]

QUOTES_PICS = list(zip(QUOTES, PICS))

def home(request):
    """the home page where it will display a random image and a random quote"""
    quote, pic = random.choice(QUOTES_PICS)
    context = {"quote": quote, "pic": pic}
    return render(request, "templates/home.html", context)

def quote(request):
    """the quote page where it will display a random quote"""
    quote = random.choice(QUOTES)
    pic = random.choice(PICS)
    context = {"quote": quote, "pic": pic}
    return render(request, "quote.html", context)

def show_all(request):
    """this page will display all quotes and images"""
    quotes = QUOTES
    pics = PICS
    return render(request, "show_all.html", {"quotes": quotes, "pics": pics})

def about(request):
    """this page will display information about the author"""
    return render(request, "about.html")