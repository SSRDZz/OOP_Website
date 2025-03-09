#Mock Code for User's tour customizing and staff confirming
from dataclasses import dataclass
from datetime import datetime
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
        self.filter = ""
        self.__currentUser = User("testUser","123")

    def AddFilter(self,filter):
        self.filter = filter
        return 

    def create_account(self, username, password):
        self.account.append(User(username, password))
        return
    
    def create_staff_account(self, username, password):
        self.account.append(Staff(username, password))
        return

    def RequestCreateTour(self,name,location, data,fname):
        t = self.tour_manager.CreateCustomizedTour(name,location)
        print(location)
        book = Booking(t,data,self.__currentUser,str(t.id)+"_"+str(fname))
        print("name : ",t.name,"location :",t.place,data,"Id :",str(t.id)+"_"+str(fname))
        self.pendingTour.append(book)

    def SearchTour(self,id="",place="",time=""): #ใส่ id -> instance tour | ใส่ที่เหลือ list instance
        return self.tour_manager.search_tour(id,place,time)
    
    def book_tour(self, tour_program, data,id):
        self.__currentUser.create_booking_tour(tour_program, data,id)
    
    def SearchPendingTour(self,tourId):
        print("Search received :",tourId)
        for i in range(len(self.pendingTour)):
            if(self.pendingTour[i].booking_id == tourId):
                print("Found pending")
                return i
            else:
                continue
    
    def ConfirmTour(self,tourId):
        i = self.SearchPendingTour(tourId)
        self.pendingTour[i].accept()
        del self.pendingTour[i]

    def DenyTour(self,tourId):
        print("denying_Id :",tourId)
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

    def generate_tour_id(self):
        return int(len(self.pendingTour))+self.tour_manager.get_tour_count()+1

class TourManager:
    def __init__(self):
        self.__tour_program = []

    def add_tour(self,tour):
        if isinstance(tour, TourProgram):
            return self.__tour_program.append(tour)
        else :
            while(1):
                print("why do you do this bro") # smoothie อย่าลืมเเก้ตอนส่ง

    def get_tour_count(self):
        return int(len(self.__tour_program))

    
    @staticmethod
    def check_time(time_in,time_check):   # time format -> DD/MM/YY - DD/MM/YY
        
        #ค่าที่เราหา
        in_start = datetime.strptime(time_in.split(" - ")[0], '%d/%m/%Y')
        in_end = datetime.strptime(time_in.split(" - ")[1], '%d/%m/%Y')

        #ตัวที่ต้องการจะไปเทียบ
        check_start = datetime.strptime(time_check.split(" - ")[0], '%d/%m/%Y')
        check_end = datetime.strptime(time_check.split(" - ")[1], '%d/%m/%Y')

        if(in_start>=check_start and in_end<=check_end):
            return True

        return False           



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
                    if(self.check_time(time,tour.time) and place.lower() in tour.place.lower()):
                        tours.append(tour)
            else:
                for tour in self.__tour_program:
                    if(self.check_time(time,tour.time)):
                        tours.append(tour)

        elif(place!=""):
            for tour in self.__tour_program:
                    if(place.lower() in tour.place.lower() ):
                        tours.append(tour)

        else:
            return self.__tour_program #กรณีไม่ใส่ input อะไรเลยให้ return ทั้งหมด
        
        return tours

    def CreateCustomizedTour(self,name,location):
        t = TourProgram(name,location)
        print("Created",name,"Id :",t.id)
        return t
    
    def get_all_tour(self):
        return self.__tour_program

class TourProgram:
    
    Travelling = []
    def __init__(self,name,place,time = 0): # time ให้เป็น 0 ไปก่อนจะเอาไปลอง code
        self.__name = name
        self.__id = website.generate_tour_id()
        self.__place = place
        self.__time = time # time formaat -> DD/MM/YY - DD/MM/YY
    
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
    @property
    def bookingList(self):
        return self.__booking
    
    @property
    def payment_list(self):
        return self.__payment
    
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
        new_booked = Booking(tour_program, data,id,self)
        self.__booking.append(new_booked)
        self.create_payment(new_booked.booking_id, new_booked)

    def add_booking(self,booking): # type: ignore
        self.__booking.append(booking)
        self.create_payment(booking.booking_id, booking)
    
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
    
    def calculate_price(self, adults, children):
        return (adults * 800) + (children * 200)
    
    def Pay(self):
        return "Success"
    

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
    def __init__(self, title, href, image, description, content=""):
        self.__title = title
        self.__href = href
        self.__image = image  # Path to the image
        self.__description = description
        self.__content = content  # Full article content

    def get_title(self):
        return self.__title

    def get_href(self):
        return self.__href

    def get_image(self):
        return self.__image

    def get_description(self):
        return self.__description

    def get_content(self):
        return self.__content

    def to_dict(self):
        return {
            "title": self.__title,
            "href": self.__href,
            "image": self.__image,
            "description": self.__description,
            "content": self.__content
        }
    

class Booking:
    def __init__(self,tour_program, data:str, id_booking:str,owner:User):
        self.__tour_program = tour_program
        self.__status : str = 'payment'    #pending payment done
        self.__data = data        # data -> "fname:{fname}|lname:{lname}|email:{email}|phone:{phone}|adult:{adult}|child:{child}" adult มากกว่า 0 คนเสมอ ราคา adult->8xx child 2xx
        self.__id = id_booking      # id -> {tour_id}+{fname} *firstname
        self.__owner = owner

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
    
    def accept(self):
        self.__owner.add_booking(self)
    
class Filter:
    def __init__(self,tour_search):
        self.__tour_search = tour_search
        self.__filter_list = []
        

    def filter_tour(self):  # filter ตาม filter ที่กรองไว้
        if(self.__filter_list == []):
            return self.__tour_search
        
        tours = []
        for tour in self.__tour_search:
            count = 0
            in_start = datetime.strptime(tour.time.replace(" ", "").split("-")[0], '%d/%m/%Y')
            in_end = datetime.strptime(tour.time.replace(" ", "").split("-")[1], '%d/%m/%Y')
            time_count = in_end - in_start

            if("3-5" in self.__filter_list and 3<= time_count.days <=5):
               count+=1
            if("sunny" in self.__filter_list and (2<=in_end.month<=5 or 2<=in_start.month<=5)):
                count +=1
            if(count == len(self.__filter_list)):
                tours.append(tour)

        return tours
    

    def append_filter(self,type): # เพิ่ม filter
        self.__filter_list.append(type)
        return self.filter_tour()

    def remove_filter(self,type): # ลบ filter
        if(type not in self.__filter_list):
            return self.filter_tour()
        else:
            self.__filter_list.remove(type)
            return self.filter_tour()
    
website = Website()
promotion = Promotion()

def create_enviroment():

    
    website.tour_manager.add_tour(TourProgram("minprogram","Thai","29/3/2025- 2/4/2025"))
    website.tour_manager.add_tour(TourProgram("zardprogram","Thai","27/2/2025- 1/3/2025"))
    website.tour_manager.add_tour(TourProgram("owenprogram","Thai","10/3/2025 - 17/3/2025"))
    # website.tour_manager.add_tour(TourProgram("owenprogram",4,"Thai","1/2/2025 - 2/2/2025"))
    website.tour_manager.add_tour(TourProgram("owenprogram","Nihongo","1/3/2025 - 30/3/2025"))
    website.tour_manager.add_tour(TourProgram("owenprogram","Russia","10/3/2025 - 15/3/2025"))
    website.tour_manager.add_tour(TourProgram("owenprogram","Germany","1/3/2025 - 3/3/2025"))
    website.tour_manager.add_tour(TourProgram("owenprogram","Thai","10/3/2025 - 20/3/2025"))
    website.tour_manager.add_tour(TourProgram("owenprogram","Israel","11/3/2025 - 18/3/2025"))
    website.tour_manager.add_tour(TourProgram("owenprogram","Thai","12/3/2025 - 15/3/2025"))
    website.tour_manager.add_tour(TourProgram("owenprogram","India","12/3/2025 - 14/3/2025"))
    website.tour_manager.add_tour(TourProgram("tonwaiprogram","Oiiaiioiiai","11/3/2025 - 13/3/2025"))
    website.tour_manager.add_tour(TourProgram("minprogram","barley_farm","1/1/1000 - 31/12/9999"))
    website.tour_manager.add_tour(TourProgram("tonwaiprogram","Ohio","11/1/2025 - 13/1/2025"))
    website.tour_manager.add_tour(TourProgram("tonwaiprogram","Nihongo","11/7/2025 - 13/7/2025"))
    website.tour_manager.add_tour(TourProgram("tonwaiprogram","Nihongo","28/11/2025 - 5/12/2025"))
    website.tour_manager.add_tour(TourProgram("jojoprogram","Ponaleffland","24/11/2025 - 28/11/2025"))


    
    website.create_account("testUser","123")
    website.TryLogIn("testUser","123")
    
    website.book_tour(website.SearchTour('1'),"fname:Susee|lname:Sereng|email:test@gmail.com|phone:09912323434|adult:1|child:2","1")
    
    print(website.SearchTour(id=1).name)

create_enviroment()