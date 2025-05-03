from abc import ABC, abstractmethod
import json 
import datetime
class Device:
    def __init__(self):
        self.temps = []
        self.thermostat = Thermostat()
        self.status = "off"
        self.consumed_energy_time = 0
    @abstractmethod
    def turn_on(self):
        if self.status=="off":
            self.status="on"
            self.time_started = datetime.datetime.now()

            print(f"{self.__class__.__name__} device in now on")
        else:
            print("device is already on")
            self.consumed_energy = datetime.datetime.now - self.time_started
    @abstractmethod
    def turn_off(self):
        if self.status == "on":
            self.status = "off"
            print("device is now off")
        else:
            print("device is already off")
    def Temperature(self,celcius):
        if celcius>=30:
            self.thermostat().turn_on()
        else:
            self.thermostat().turn_off
        self.temps.append(celcius)
    def temperature_change(self):
        import matplotlib.pyplot as plt 
        fig, ax = plt.subplots(1,1,figsize = (10,6))
        ax[0,0].plot([],self.temps)


class Light(Device):
    def __init__(self):
        self.status = "off"
    def turn_on(self):
        return super().turn_on()
    def turn_off(self):
        return super().turn_off()
class Thermostat(Device):
    def __init__(self):
        self.status = "off"
    def turn_on(self):
        return super().turn_on()
    def turn_off(self):
        return super().turn_off()
class Camera(Device):
    def __init__(self):
        self.status = "off"
    def turn_on(self):
        return super().turn_on()
    def turn_off(self):
        return super().turn_off()
class Alarm(Device):
    def __init__(self):
        self.status = "off"
    def turn_on(self):
        return super().turn_on()
    def turn_off(self):
        return super().turn_off()

# light = Light()

# light.turn_on()

      

