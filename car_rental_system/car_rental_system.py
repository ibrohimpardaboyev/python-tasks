import json
from abc import ABC, abstractmethod
import logging
import datetime

logging.basicConfig(filename='rental.log', level=logging.INFO)

def today_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

class Vehicle:
    def __init__(self,name, price):
        self.name = name 
        self.price = price 
        self.is_rent = False
        self.rent_count = 0
    @abstractmethod
    def rent(self):
        pass

    @abstractmethod
    def rent_return(self):
        pass
    @abstractmethod
    def rent_count(self):
        pass
class Car(Vehicle):
    def rent(self):
        if self.is_rent:
            print(f"{self.name} was already rent")
        else:
            logging.info(f"{self.name} was rent at {today_date()}")
            self.is_rent=True 
            self.rent_count += 1 
    def rent_return(self):
        self.is_rent = False
    def rent_calculate(self,days):
        rate = self.price 
        if self.rent_count >= 3:
            rate *= 0.9
        return rate*days
    
class Truck(Vehicle):
    def rent(self):
        if self.is_rent:
            print(f"{self.name} was already rent")
        else:
            logging.info(f"{self.name} was rent at {today_date()}")
            self.is_rent=True 
            self.rent_count += 1 
    def rent_return(self):
        self.is_rent = False
    def rent_calculate(self,days):
        rate = self.price 
        if self.rent_count >= 3:
            rate *= 0.9
        return rate*days
class Bike(Vehicle):
    def rent(self):
        if self.is_rent:
            print(f"{self.name} was already rent")
        else:
            logging.info(f"{self.name} was rent at {today_date()}")
            self.is_rent=True 
            self.rent_count += 1 
    def rent_return(self):
        self.is_rent = False
    def rent_calculate(self,days):
        rate = self.price 
        if self.rent_count >= 3:
            rate *= 0.9
        return rate*days

class FleetManager:
    def __init__(self):
        self.vehicle = {}
    def add_vehicle(self,vehicle):
        self.vehicle[vehicle.name] = vehicle 
    def save_to_json(self,filename):
        data = {
            name: {
                'name': name,
                'price': v.price,
                'is_rent': v.is_rent,
                'rent_count': v.rent_count,
                'type': v.__class__.__name__
            } for name,v in self.vehicle.items()
        }
        with open(filename, "w") as file:
            json.dump(data,file,indent=4)
    def load_from_file(self,filename):
        with open(filename, "r") as file:
            data = json.load(file)
        for v in data:
            vehicle = data[v]
            vehicle_type = {"Bike":Bike, "Car":Car, "Truck": Truck}
            name = vehicle['name']
            price = vehicle['price']
            type = vehicle['type']
            is_rent = vehicle['is_rent']
            rent_count = vehicle['rent_count']
            veh = vehicle_type[type](name,price)
            veh.is_rent = is_rent
            veh.rent_count = rent_count
    def search(self, **kwargs):
        results = []
        for veh in self.vehicle.values():
            if all(getattr(veh, k) == v for k, v in kwargs.items()):
                results.append(veh)
        return results
            
# manager = FleetManager()
# manager.load_from_file("vehicles.json")
# manager.add_vehicle(Car("BMW", 20000))
# manager.vehicle['BMW'].rent()
# manager.vehicle['BMW'].rent_return()
# manager.vehicle['BMW'].is_rent
# manager.vehicle['BMW'].price
# manager.save_to_json("vehicles.json")
# manager.search(name = "BMW")
