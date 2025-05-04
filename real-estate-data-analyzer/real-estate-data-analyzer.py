from abc import ABC, abstractmethod
import pandas as pd
import seaborn as sns
class PropertyManager:
    def __init__(self, file='properties_data.csv'):
        self.file = file
        try:
            self.properties = pd.read_csv(file)
        except FileNotFoundError:
            self.properties = pd.DataFrame(columns=["property", "area", "district", "room count", "price", "is_sold"])
    
    def add_property(self, property):
        new_row = {
            "property": property.__class__.__name__,
            "area": property.area,
            "district": property.district,
            "room count": property.room_cnt,
            "price": property.price,
            "is_sold": False
        }
        self.properties.loc[len(self.properties)] = new_row
        self.save()
    
    def save(self):
        self.properties.to_csv(self.file, index=False)
    
    def get_stats(self):
        avg_price = self.properties["price"].mean()
        most_expensive_area = self.properties.sort_values(by="price", ascending=False).iloc[0]['district']
        sold_count = len(self.properties[self.properties["is_sold"] == True])
        return f"Average Price: {avg_price:.2f}\nMost Expensive Area: {most_expensive_area}\nTotal Sold: {sold_count}"
    
    def mark_sold(self, index):
        self.properties.at[index, "is_sold"] = True
        self.save()

    def calculate_price_per_m2(self):
        df = self.properties.copy()
        df['price_per_m2'] = df['price'] / df['area']
        return df[['property', 'district', 'area', 'price', 'price_per_m2']]

class AbstractProperty(ABC):
    @abstractmethod
    def __init__(self, district, area, room_cnt, price):
        self.district = district
        self.area = area
        self.room_cnt = room_cnt
        self.price = price
        self.is_sold = False

class Appartment(AbstractProperty):
    def __init__(self, district, area, room_cnt, price):
        super().__init__(district, area, room_cnt, price)

class House(AbstractProperty):
    def __init__(self, district, area, room_cnt, price):
        super().__init__(district, area, room_cnt, price)

class FilterStrategy:
    def apply(self, df):
        raise NotImplementedError()

class PriceFilter(FilterStrategy):
    def __init__(self, min_price, max_price):
        self.min_price = min_price
        self.max_price = max_price

    def apply(self, df):
        return df[(df['price'] >= self.min_price) & (df['price'] <= self.max_price)]

class RoomCountFilter(FilterStrategy):
    def __init__(self, min_rooms, max_rooms):
        self.min_rooms = min_rooms
        self.max_rooms = max_rooms

    def apply(self, df):
        return df[(df['room count'] >= self.min_rooms) & (df['room count'] <= self.max_rooms)]
def plot_price_distribution(df = pd.read_csv("properties_data.csv")):
    sns.histplot(df['price'], kde=True)
    plt.title("Price Distribution")
    plt.xlabel("Price")
    plt.ylabel("Count")
    plt.show()
