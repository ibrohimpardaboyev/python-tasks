import json
import pandas as pd
class User:
    def __init__(self):
        with open("users.json","r") as file:
            data = json.load(file)
        self.data = data
        self.session=None
    def login(self,user_name,password):
        data = self.data
        if user_name in data and data[user_name]['password']==password:
            print("login successull")
            self.session = user_name
        else:
            print("user_name or ")
    def signup(self,user_name,full_name,password):
        if user_name in self.data:
            print("username already exsits")
        else:
            self.data[user_name] = {"password":password,"fullname": full_name}
            with open("users.json","w") as file:
                json.dump(self.data,file)
    def info(self):
        data = self.data[self.session]
        print(f"user_name: {self.session}\nfullname {data['fullname']}")
class Book:
    def __init__(self,name,author,year,genre,*args):
        self.name = name 
        self.author = author
        self.year = year
        self.genre = genre
        self.is_rent=False
        self.rent_count = 0
        if len(list(args))==2:
            self.is_rent = list(args)[0]
            self.rent_count = list(args)[1]
    def rent(self,user: User):
        if self.is_rent == False:
            if user.session:
                print(f"book was rent by {user.session}")
                self.is_rent = True 
                self.rent_count += 1
            else:
                print("please input a correct account or if you don't have please signup")
        else:
            print("book was already rent by another user")
    def rent_return(self):
        self.is_rent = False

class Library:
    def __init__(self):
        self.books={}
    def add_book(self,book: Book):
        self.books[book.name] = book
    def search_book(self,**kwargs):
        with open("books_data.json") as file:
            data = json.load(file)
        for vals in data.values():
            supplied=0
            required=len(kwargs)
            for i in kwargs:
                try:
                    if kwargs[i] == vals[i]:
                        supplied+=1
                except:
                    print(f"function cannot get argument {i}")
                    return
            if required == supplied:
                print(vals)
    def save_to_file(self,filename):
        data = {
            name: {
                "name": book.name,
                "author": book.author,
                "year": book.year,
                "genre": book.genre,
                "is_rent": book.is_rent,
                "rent_count": book.rent_count
            } for name,book in self.books.items()
        }
        with open(filename,"w") as file:
            json.dump(data,file)
    def load_data(self,filename):
        with open(filename,"r") as file:
            books=json.load(file)
        for name, book in books.items():
            self.books[name] = Book(book["name"],book["author"],book["year"],book["genre"],book["is_rent"],book["rent_count"])
class Admin:
    def __init__(self):
        pass
    def statistiks(self) -> pd.DataFrame:
        with open("books_data.json","r") as file:
            data = json.load(file)
        stats = {
            "name": [],
            "author": [],
            "year": [],
            "genre": [],
            "rent_count": []
        }
        for rows in data.values():
            stats['name'].append(rows['name'])
            stats['author'].append(rows['author'])
            stats['year'].append(rows['year'])
            stats['genre'].append(rows['genre'])
            stats['rent_count'].append(rows['rent_count'])
        return pd.DataFrame(stats).sort_values(by="rent_count")
library = Library()
# library.add_book(Book("harry potter","Jim Collins",2010,"fantacy"))
# library.save_to_file("books_data.json")
# library.load_data("books_data.json")
# user = User()
# user.signup('pardaboyevime','Ibrohim Pardaboyev','ibrohim')
# user.login('pardaboyevime','ibrohim')
# library.books['harry potter'].rent(user)
# library.save_to_file("books_data.json")
# admin = Admin()
# print(admin.statistiks())
# library.load_data("books_data.json")
# library.search_book(author="Jim Collins", genre = "fantacy")
