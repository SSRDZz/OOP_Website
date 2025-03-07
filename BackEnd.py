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

    @property
    def currentUser(self): return self.__currentUser
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Website, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.tour_manager = TourManager()
        self.__currentUser = User("testUser","123")

    def create_account(self, username, password):
        self.account.append(User(username, password))
        return
    
    def create_staff_account(self, username, password):
        self.account.append(Staff(username, password))
        return

    def RequestCreateTour(self,name,location):
        self.pendingTour.append(self.tour_manager.CreateCustomizedTour(name,location))

    def SearchTour(self,id="",place="",time=""): #ใส่ id -> instance tour | ใส่ที่เหลือ list instance
        return self.tour_manager.search_tour(id,place,time)
    
    def booking_tour(self, tour_program, data,id):
        return self.__currentUser.create_booking_tour(tour_program, data,id)
    
    def SearchPendingTour(self,tourId):
        print("Search received :",tourId)
        for i in range(len(self.pendingTour)):
            if(self.pendingTour[i].id == tourId):
                print("Found pending")
                return i
            else:
                continue
    
    def ConfirmTour(self):
        pass

    def DenyTour(self,tourId):
        i = self.SearchPendingTour(tourId)
        del self.pendingTour[i]

    def TryLogIn(self,username, password):
        for acc in self.account:
            if(acc.verify(username,password) == True):
                self.__currentUser = acc
                print("user LogIn : ",acc.username)
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
        print("Created",name,"Id :",t.id)
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
    
    def RequestCreateTour(self,name,location):
        pass

class User(Account):
    def __init__(self,name,password):
        self.__booking = []
        self.__payment = []
        super().__init__(name,password)
        print("User created :",self.username)

    def RequestCreateTour(self,name,location):
        website.RequestCreatTour(self,name,location)

    def talk(self):
        print("Created User")

    def create_payment(self, transaction_id:str, booked:'Booking'):
        self.__payment.append(Payment(transaction_id, booked))

    def create_booking_tour(self,tour_program : TourProgram, data:str,id:str):
        new_booked = Booking(tour_program, data,id)
        self.__booking.append(new_booked)
        self.create_payment(new_booked.booking_id, new_booked)
    
    def search_booking(self,id):
        for booking in self.__booking:
            if booking.booking_id == id:
                return booking
        return None
    
    def search_payment(self, id):
        for payment in self.__payment:
            if payment.transaction_id == id:
                return payment
        return None
    
    @property
    def bookingList(self):
        return self.__booking
    
    @property
    def payment_list(self):
        return self.__payment
    

class Staff(Account):
    def __init__(self,name,password):
        super().__init__(name,password)
        print("Staff created",self.username)

    def SearchPendingTour(self,tourName):
        pass

    def ConfirmTour(self,tourInstance):
        pass

class Payment():
    def __init__(self, transaction_id:str, booking:'Booking'):
        self.__triansaction_id = transaction_id
        self.__payment_method = None #str
        self.__booking = booking
        self.__net_price = 0
    
    @property
    def net_price(self): return self.__net_price
    
    @net_price.setter
    def net_price(self,amount): self.__net_price = amount
            
    @property
    def transaction_id(self): return self.__triansaction_id
    
    @property
    def payment_method(self): return self.__payment_method
    
    @payment_method.setter
    def payment_method(self, method):
        self.__payment_method = method
    
    
class Promotion:
    def __init__(self):
        self.__summer_tour = []
        self.__winter_tour = []
        self.__fall_tour = []
        self.__autumn_tour = []
    
    def add_tour(self, tour: TourProgram, season: str):
        match season:
            case "summer":
                self.__summer_tour.append(tour)
            case "winter":
                self.__winter_tour.append(tour)
            case "fall":
                self.__fall_tour.append(tour)
            case "autumn":
                self.__autumn_tour.append(tour)
            case _:
                return "Error: cannot add tour to discount"
        return "Discount added"

    
    def get_discount(self, tour:TourProgram):
        for program in self.__summer_tour:
            if tour == program:
                return float(10)
        for program in self.__winter_tour:
            if tour == program:
                return float(10)
        for program in self.__fall_tour:
            if tour == program:
                return float(10)
        for program in self.__autumn_tour:
            if tour == program:
                return float(10)
        return float(0)
    
    
class Article:
    """ Represents an article with title, href, image, and description """
    def __init__(self, title, href, image, description):
        self.title = title
        self.href = href
        self.image = image  # Path to the image
        self.description = description

    def to_dict(self):
        """ Converts object to dictionary format for rendering """
        return {
            "title": self.title,
            "href": self.href,
            "image": self.image,
            "description": self.description
        }

class Booking:
    def __init__(self,tour_program, data:str, id_booking:str):
        self.__tour_program = tour_program
        self.__status : str = 'payment'    #pending payment done
        self.__data = data        # data -> "fname:{fname}|lname:{lname}|email:{email}|phone:{phone}|adult:{adult}|child:{child}" adult มากกว่า 0 คนเสมอ ราคา adult->8xx child 2xx
        self.__id = id_booking      # id -> {tour_id}+{fname} *firstname

    @property
    def tour_program(self):
        return self.__tour_program

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def update_status(self,status:str):
        self.__status = status
        
    @property
    def booking_id(self):
        return self.__id    
    
    @property
    def data(self):
        return self.__data 
    
website = Website()
promotion = Promotion()

def create_enviroment():

    
    website.tour_manager.add_tour(TourProgram("minprogram",1,"Thai"))
    website.tour_manager.add_tour(TourProgram("zardprogram",2,"Thai"))
    website.tour_manager.add_tour(TourProgram("owenprogram",3,"Thai"))
    website.tour_manager.add_tour(TourProgram("owenprogram",4,"Thai"))
    website.tour_manager.add_tour(TourProgram("owenprogram",5,"Nihongo"))
    website.tour_manager.add_tour(TourProgram("owenprogram",6,"Russia"))
    website.tour_manager.add_tour(TourProgram("owenprogram",7,"Germany"))
    website.tour_manager.add_tour(TourProgram("owenprogram",8,"Thai"))
    website.tour_manager.add_tour(TourProgram("owenprogram",9,"Israel"))
    website.tour_manager.add_tour(TourProgram("owenprogram",10,"Thai"))
    website.tour_manager.add_tour(TourProgram("owenprogram",11,"India"))


    
    website.create_account("testUser","123")
    website.TryLogIn("testUser","123")
    
    website.booking_tour(website.tour_manager.search_tour('1'),None,"1_Min")
    website.booking_tour(website.tour_manager.search_tour('4'),None,"4_Owen")
    
    print(website.SearchTour(id=1).name)

create_enviroment()