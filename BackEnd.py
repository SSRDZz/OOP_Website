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
    tourProgram = []
    def __init__(self):
        self.tourProgram.append(TourProgram("Tour1"))
        self.tourProgram.append(TourProgram("Tour2"))

    def CreateCustomizedTour(self,name):
        t = TourProgram(name)
        print("Created",name)
        return t

class TourProgram:
    Travelling = []
    def __init__(self,name):
        self.name = name

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
