#Mock Code for User's tour customizing and staff confirming
from dataclasses import dataclass
@dataclass
class Website:
    # Singleton instance
    _instance = None
    
    # Class-level variables
    pendingTour = []
    tourManager = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Website, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.tourManager = TourManager()

    def RequestCreateTour(self,name):
        self.pendingTour.append(self.tourManager.CreateCustomizedTour(name))

    def SearchTour(self):
        return "TourProgram Instance"
    
    def SearchPendingTour(self):
        return self.pendingTour
    
    def ConfirmTour(self):
        pass

class TourManager:
    def __init__(self):
        self.__tour_program = []

    def add_tour(self,tour):
        if isinstance(tour, TourProgram):
            return self.__tour_program.append(tour)
        else :
            while(1):
                print("why do you do this bro") # smoothie อย่าลืมเเก้ตอนส่ง

    def search_tour(self,id,place,time):
        if(id!=None):
            pass #return only one instance
        else:
            return self.append_tour(place,time) # return list instance


    def append_tour(self,place,time):
        if(time!=None):
            if(place!=None):
                pass
            else:
                pass

        elif(place!=None):
            pass

    def CreateCustomizedTour(self,name):
        t = TourProgram(name)
        print("Created",name)
        return t

class TourProgram:
    Travelling = []
    def __init__(self,name,id,place,time = 0): # time ให้เป็น 0 ไปก่อนจะเอาไปลอง code
        self.name = name
        self.__id = ''
        self.__place = ''
        self.__time = ''

class Travelling:
    startLoacation = None
    endLocation = None
    def __init__(self):
        pass

class Account:
    def __init__(self):
        pass

class User(Account):
    def __init__(self):
        pass

    def CreateTour(self):
        website.RequestCreatTour()

    def talk(self):
        print("Created User")

class Staff(Account):
    def __init__(self):
        pass

    def SearchPendingTour(self,tourName):
        pass

    def ConfirmTour(self,tourInstance):
        pass

class Payment():
    def __init__(self):
        pass
    
    def Pay():
        pass
    


website = Website()
