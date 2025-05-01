import json 
import datetime
from datetime import timedelta
import logging

logging.basicConfig(
    filename="logHotel.log",       # Log file name
    filemode="a",                    # 'a' for append, 'w' for overwrite
    level=logging.INFO,              # Minimum level to log
    format="%(asctime)s - %(levelname)s - %(message)s"
)
class Hotel:
    def add_room(self,room_number, type, price_per_day):
        with open("hotel_room_data.json", "r") as file:
            data = json.load(file)
        data[room_number] = {"type": type, "price":price_per_day}
        with open("hotel_room_data.json","w") as file:
            json.dump(data,file)
    def update_price(self,room_number, new_price):
        with open("hotel_room_data.json", "r") as file:
            data = json.load(file)
        data[room_number]['price'] = new_price
        with open("hotel_room_data.json","w") as file:
            json.dump(data,file)
    pass
class Customer:
    def __init__(self,customer_name,age,gender, customer_uuid):
        self.customer_name = customer_name
        self.customeruuid = customer_uuid
        self.age = age 
        self.gender = gender
    def update_details(self,**kwargs) -> None:
        for i in kwargs:
            self[i] = kwargs[i]
    def info(self):
        logging.info(f"customer Name: {self.customer_name}\nage: {self.age}\ngender: {self.gender}")
    
class Room:
    def __init__(self,room_number,customer: Customer):
        self.room_number = room_number
        self.customer_name = customer.customer_name
        self.customeruuid = customer.customeruuid
        self.age = customer.age
        self.gender = customer.gender
    def search(self, date) -> int:
        with open("hotel_room_data.json","r") as file:
            data = json.load(file)
        with open("booked_days.json", "r") as file:
            book_dates = json.load(file)
        search_result = {}
        for room_number, info in data.items():
            dates=sorted(book_dates.get(room_number, []))
            if date not in dates:
                search_result[room_number] = info
        return search_result
    def Book(self,date) -> None:
        with open("booked_days.json", "r") as file:
            book_dates = json.load(file)
        target_room = book_dates.get(self.room_number, [])
        target_room.append(date)
        book_dates[self.room_number] = target_room 
        print(f"room with number {self.room_number} booked on {date} date succesfully by {self.customer_name}")
        with open("booked_days.json","w") as file:
            json.dump(book_dates,file)
                        
            
class Admin:
    def __init__self():
        pass
    def revenue_report(self):
        with open("booked_days.json","r") as file:
            data = json.load(file)
        with open("hotel_room_data.json","r") as file:
            rooms_data = json.load(file)
        days={

        }
        monthly = {

        }
        for room_number,info in data.items():
            for dates in info:
                year = dates.split('-')[0]
                month = dates.split('-')[1]
                day = dates.split('-')[2]
                day_rev= days.get(day,0)
                days[day]=day_rev+rooms_data[room_number]['price']
                month_rev= monthly.get(month,0)
                monthly[month]=month_rev+rooms_data[room_number]['price']
        print("daily", days)
        print("monthly report", monthly)

hotel = Hotel()
room1 = Room(1,Customer('Ibrohim Pardaboyev',17,"male","asdpoi1#@iosdfnasd"))
print(room1.search('2025-02-30'))
# room1.Book("2025-02-30")
admin = Admin()
admin.revenue_report()
