from unicodedata import name
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from numpy import roll
from .models import Publish, collection, Student
import cv2
import os
from pyzbar.pyzbar import decode


def home(request):
    all_publishes = Publish.objects.all()
    all_publishes_count = Publish.objects.count()
    no_of_genres = collection.objects.count()
    no_of_books = Publish.objects.filter(publish_type = "Book").count()
    no_of_articles = Publish.objects.filter(publish_type = "Article").count()
    no_of_magazines = Publish.objects.filter(publish_type = "Magazine").count()
    no_of_projects = Publish.objects.filter(publish_type = "Project_files").count()
    params = {
        "all_things": all_publishes,
        "publishes_count": all_publishes_count,
        "genres_count": no_of_genres,
        "books_count": no_of_books,
        "articles_count": no_of_articles,
        "magazines_count": no_of_magazines,
        "projects_count": no_of_projects,  
    }
    return render(request, '/Work/MiniProject/Library/templates/home.html', params)

def logged_home(request, logged_user):
    return render(request, '/Work/MiniProject/Library/templates/logged_home.html')

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/")
    return render(request, '/Work/MiniProject/Library/templates/login.html')

def readcode(request):
    book_name = request.POST.get("book_name")
    author_name = request.POST.get("author_name")
    edition = request.POST.get("edition")
    quantity = request.POST.get("quantity")
    genres = request.POST.get("genres")
    type_ = request.POST.get("type")
    print(book_name)
    print(author_name)
    print(edition)
    print(quantity)
    print(genres)
    print(type_)
    img = cv2.imread("media/scanned_image.jpg")
    id = ""
    for code in decode(img):
        id += code.data.decode('utf-8')
    new_publish = Publish(name=book_name, author=author_name, Edition=edition, id=id, quantity=quantity, publish_type=type_)
    new_genre = collection.objects.get(genre = genres)
    os.remove("media/scanned_image.jpg")
    if id == "":
        return HttpResponseRedirect("/add/fail")
    new_publish.book_genre = new_genre
    new_publish.save()
    return HttpResponseRedirect("/add/success")

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")

def collections(request):
    return render(request, '/Work/MiniProject/Library/templates/collections.html')

def add(request):
    params = {
        "genres": collection.objects.all(),
    }
    return render(request, "/Work/MiniProject/Library/templates/add.html", params)

def borrow(request, roll=""):
    # print("------->" + roll)
    borrower = Student.objects.get(roll_no = roll)
    b_name = borrower.name
    b_mobile = borrower.mobile_no
    books_borrowed = borrower.no_of_borrowers.all()
    params = {
        "borrower_roll": roll,
        "borrower_name": b_name,
        "borrower_mobile": b_mobile,
        "borrowed_books": books_borrowed,
    }
    print(roll, b_name, b_mobile, books_borrowed)
    return render(request, "/Work/MiniProject/Library/templates/borrow.html", params)

def add_book(request, b_roll=""):
    img = cv2.imread("media/scanned_image.jpg")
    book_id = ""
    for code in decode(img):
        book_id += code.data.decode('utf-8')
    os.remove("media/scanned_image.jpg")
    try:
        book_to_borrow = Publish.objects.get(id = book_id)
    except Publish.DoesNotExist:
        return HttpResponseRedirect(f"/borrow/{b_roll}")
    borrower = Student.objects.get(roll_no = b_roll)
    books_borrowed = borrower.no_of_borrowers.all()
    if book_to_borrow in books_borrowed:
        book_to_borrow.borrowers.remove(borrower)
    else:
        book_to_borrow.borrowers.add(borrower)
    return HttpResponseRedirect(f"/borrow/{b_roll}")

def student_scanner(request):
    img = cv2.imread("media/scanned_image.jpg")
    roll = ""
    for code in decode(img):
        roll += code.data.decode('utf-8')
    os.remove("media/scanned_image.jpg")
    if roll == "":
        return HttpResponseRedirect("/student_scan")
    return HttpResponseRedirect(f"/borrow/{roll}")

def student_scan(request):
    return render(request, "/Work/MiniProject/Library/templates/student_scan.html")