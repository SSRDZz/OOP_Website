#Mock Code for User's tour customizing and staff confirming
from dataclasses import dataclass
@dataclass
class Website:
    # Singleton instance
    _instance = None
    
    # Class-level variables
    pendingTour = []
    tour_manager = None

    # Store account
    account = []
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Website, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.__user = []
        self.tour_manager = TourManager()

    def create_account(self, username, password):
        self.account.append(Account(username, password))
        return

    def RequestCreateTour(self,name,location):
        self.pendingTour.append(self.tour_manager.CreateCustomizedTour(name,location))

    def SearchTour(self,id="",place="",time=""): #ใส่ id -> instance tour | ใส่ที่เหลือ list instance
        return self.tour_manager.search_tour(id,place,time)
    
    def booking_tour(self, user, tour_program, data):
        return user.create_booking_tour(tour_program, data)
    
    def SearchPendingTour(self):
        return self.pendingTour
    
    def ConfirmTour(self):
        pass

    def TryLogIn(self,username, password):
        for acc in self.account:
            if(acc.verify(username,password) == True):
                return True
            else:
                continue
        return False
    
    def search_user(self,user_id):
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

    def search_tour(self,id="",place="",time=""):
        if(id!=""):
            for tour in self.__tour_program: #return only one instance
                if(str(id)==str(tour.id)): # น่าจะต้อง encap____________________
                    
                    return tour
            else:
                return None # ไม่เจอ 
            
        else:
            return self.search_list_tour(place,time) # return list instance


    def search_list_tour(self,place="",time=""):
        tours = []

        if(time!=""):
            if(place!=""):
                for tour in self.__tour_program:
                    if(time==tour.time and place.lower() in tour.place.lower()):
                        tours.append(tour)
            else:
                for tour in self.__tour_program:
                    if(time==tour.time ):
                        tours.append(tour)

        elif(place!=""):
            for tour in self.__tour_program:
                    if(place.lower() in tour.place.lower() ):
                        tours.append(tour)

        else:
            return self.__tour_program #กรณีไม่ใส่ input อะไรเลยให้ return ทั้งหมด
        
        return tours

    def CreateCustomizedTour(self,name,location):
        t = TourProgram(name,str(len(self.__tour_program)),location)
        print("Created",name)
        return t
    
    def get_all_tour(self):
        return self.__tour_program

class TourProgram:
    
    Travelling = []
    def __init__(self,name,id,place,time = 0): # time ให้เป็น 0 ไปก่อนจะเอาไปลอง code
        self.__name = name
        self.__id = id
        self.__place = place
        self.__time = time
    
    @property
    def id(self):
        return self.__id
    @property
    def place(self):
        return self.__place
    @property
    def name(self):
        return self.__name
    @property
    def time(self):
        return self.__time

class Travelling:
    startLoacation = None
    endLocation = None
    def __init__(self):
        pass

class Account:
    @property
    def username(self):return self.__username
    @property
    def password(self):return self.__password

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def verify(self, username, password):
        if username == self.__username and password == self.__password:
            return True
        return False

class User(Account):
    def __init__(self):
        self.__booking = []

    def CreateTour(self):
        website.RequestCreatTour()

    def talk(self):
        print("Created User")

    def create_booking_tour(self,tour_program, data):
        try:
            # สร้าง booking ตามเงื่อนไขสักอย่าง bogo = Booking(tour_program, datatour_program, data)
            pass
  
            self.__booking.append(Booking)
            return True
        
        except : 
            return False


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

class Article:
    def __init__(self, title, href, image, description):
        self.title = title
        self.href = href
        self.image = image #path to that image
        self.description = description

class Booking:
    def __init__(self,tour_program, data):
        self.__tour_program = tour_program
        self.__data = data



website = Website()

def create_enviroment():

    website.tour_manager.add_tour(TourProgram("minprogram",1,"Thai"))
    website.tour_manager.add_tour(TourProgram("zardprogram",2,"Thai"))
    website.tour_manager.add_tour(TourProgram("owenprogram",3,"Thai"))

    print(website.SearchTour(id=1).name)

create_enviroment()