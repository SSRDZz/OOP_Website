#Mock Code for User's tour customizing and staff confirming
from dataclasses import dataclass
from datetime import datetime
from abc import ABC

@dataclass
class Website:
    # Singleton instance
    _instance = None
    
    # Class-level variables
    pending_tour = []
    tour_manager = None
    promotion = None
    articles = []
    # Store account -> List[User,Staff]
    account = []

    @property
    def current_user(self): return self.__current_user
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Website, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.tour_manager = TourManager()
        self.filter = ""
        self.__current_user = None   #For Debug    #ต้องลบ User("testUser","123")   ออกตอนส่ง
        self.promotion = Promotion()

    def add_filter(self,tours):
        self.filter = Filter(tours) 

    def create_account(self, username, password):
        self.account.append(User(username, password))
        return
    
    def create_staff_account(self, username, password):
        self.account.append(Staff(username, password))
        return

    def request_create_tour(self,name,location, data,fname,time):
        t = self.tour_manager.create_customized_tour(name,location,time)
        print(location)
        book = Booking(t,data,str(t.id)+"_"+str(fname),self.__current_user)
        print("name : ",t.name,"location :",t.place,data,"Id :",str(t.id)+"_"+str(fname),time)
        book.update_status = 'pending'
        
        self.current_user.add_booking(book)
        self.pending_tour.append(book)

    def search_tour(self,id="",place="",time=""): #ใส่ id -> instance tour | ใส่ที่เหลือ list instance
        return self.tour_manager.search_tour(id,place,time)
    
    def book_tour(self, tour_program, data,id):
        self.__current_user.create_booking_tour(tour_program, data,id)
    
    def search_pending_tour(self,tour_id):
        print("Search received :",tour_id)
        for i in range(len(self.pending_tour)):
            if(self.pending_tour[i].booking_id == tour_id):
                print("Found pending")
                return i
            else:
                continue
    
    def confirm_tour(self,tour_id):
        i = self.Search_pending_tour(tour_id)
        self.pending_tour[i].accept()
        del self.pending_tour[i]
        

    def deny_tour(self,tour_id):
        print("denying_Id :",tour_id)
        i = self.search_pending_tour(tour_id)
        self.pending_tour[i].deny()
        del self.pending_tour[i]
        

    def try_log_in(self,username, password):
        for acc in self.account:
            if(acc.verify(username,password) == True):
                self.__current_user = acc
                print("user LogIn : ",acc.username)
                return True
            else:
                continue
        return False

    def generate_tour_id(self):
        return str(int(len(self.pending_tour))+self.tour_manager.get_tour_count()+1)

class TourManager:
    def __init__(self):
        self.__tour_program = []

    def add_tour(self,tour):
        if isinstance(tour, TourProgram):
            self.__tour_program.append(tour)

    def get_tour_count(self):
        return int(len(self.__tour_program))

    
    @staticmethod
    def check_time(time_in,tour_check_time):   # time format -> DD/MM/YY - DD/MM/YY
        
        #ค่าที่เราหา
        in_start = datetime.strptime(time_in.split(" - ")[0], '%d/%m/%Y')
        in_end = datetime.strptime(time_in.split(" - ")[1], '%d/%m/%Y')

        #ตัวที่ต้องการจะไปเทียบ
        check_start, check_end = tour_check_time.change_time_to_datetime()
   
        if(in_start>=check_start and in_end<=check_end): #เช็คว่าอยู่ในช่วงไหม
            return True

        return False           



    def search_tour(self,id="",place="",time=""):
        if(id!=""):
            for tour in self.__tour_program: #return only one instance
                if(tour.check_id(id)):
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
                    if(self.check_time(time,tour) and place.lower() in tour.place.lower()):
                        tours.append(tour)
            else:
                for tour in self.__tour_program:
                    if(self.check_time(time,tour)):
                        tours.append(tour)

        elif(place!=""):
            for tour in self.__tour_program:
                    if(place.lower() in tour.place.lower() ):
                        tours.append(tour)

        else:
            return self.__tour_program #กรณีไม่ใส่ input อะไรเลยให้ return ทั้งหมด
        
        return tours

    def create_customized_tour(self,name,location,time):
        t = TourProgram(name,location,time)
        print("Created",name,"Id :",t.id)
        return t
    
    def get_all_tour(self): # return all the tour
        return self.__tour_program

class TourProgram:
    
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
    
    def check_id(self,id:str):
        return self.__id == id
    
    def change_time_to_datetime(self):
        in_start = datetime.strptime(self.time.replace(" ", "").split("-")[0], '%d/%m/%Y')
        in_end = datetime.strptime(self.time.replace(" ", "").split("-")[1], '%d/%m/%Y')
        return in_start,in_end

    def compare_month(self,month_in,month_out):
        in_start,in_end = self.change_time_to_datetime()
        return month_in <= in_start.month <= month_out or month_in <= in_end.month <= month_out

    def compare_day(self,day_in,day_out):
        in_start,in_end = self.change_time_to_datetime()
        return day_in <= in_end-in_start <= day_out


class Account(ABC):
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
    def booking_list(self):
        return self.__booking
    
    @property
    def payment_list(self):
        return self.__payment
    
    def __init__(self,name,password):
        self.__booking = []
        self.__payment = []
        super().__init__(name,password)
        print("User created :",self.username)

    def request_create_tour(self,name,location):
        website.request_create_tour(self,name,location)

    def create_payment(self, transaction_id:str):
        self.__payment.append(Payment(transaction_id))

    def create_booking_tour(self,tour_program : TourProgram, data:str,id:str): 
        new_booked = Booking(tour_program, data,id,self)
        self.__booking.append(new_booked)
        self.create_payment(new_booked.booking_id)

    def add_booking(self,booking): 
        self.__booking.append(booking)
        self.create_payment(booking.booking_id)
        for b in self.__booking:
            print("now have :",b.booking_id)
    
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



class Payment():
    def __init__(self, transaction_id:str):
        self.__triansaction_id = transaction_id
        self.__payment_method = None #str
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
    
    def pay(self):
        return "Success"
    

class Promotion:
    def __init__(self):
        self.__discounted_tour = []
        
    def add_tour(self, tour_id: str):
        
        tour = website.search_tour(tour_id)
        self.__discounted_tour.append(tour)

        return "Discount added"

    def get_discount(self, tour:TourProgram):
        for program in self.__discounted_tour:
            if tour == program:
                return float(10)
        return float(0)
    

class Booking:
    def __init__(self,tour_program, data:str, id_booking:str,owner:User):
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
    
    def accept(self):
        self.update_status = 'payment'
    
    def deny(self):
        del self
    
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
            
            if("3-5" in self.__filter_list and tour.compare_month(3,5)):
               count+=1
            if("sunny" in self.__filter_list and tour.compare_month(2,5)):
                count +=1
            if("pro" in self.__filter_list and website.promotion.get_discount(tour) == float(10)):
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

class Location:
    def __init__(self, name, description):
        self.__name = name
        self.__description = description
        self.__ratings = []

    @property
    def get_name(self):
        return self.__name

    @property
    def get_description(self):
        return self.__description

    def add_rating(self, rating):
        if 1 <= rating <= 5:
            self.__ratings.append(rating)

    def get_average_rating(self):
        if not self.__ratings:
            return 0
        return sum(self.__ratings) / len(self.__ratings)

    def to_dict(self):
        return {
            "name": self.__name,
            "description": self.__description,
            "average_rating": self.get_average_rating()
        }

class Article:

    def __init__(self, title, href, image, description, content="", rating=0, locations=None):
        self.__title = title
        self.__href = href
        self.__image = image
        self.__description = description
        self.__content = content
        self.__rating = rating
        self.__locations = locations if locations else []

    @staticmethod
    def add_article(title, href, image_path, description, content, rating, locations=None):
        sanitized_href = href.lower().replace(" ", "-")
        new_article = Article(title, sanitized_href, image_path, description, content, rating, locations)
        website.articles.append(new_article)

    @staticmethod
    def find_article_by_href(href):
        href = href.lower()
        return next((article for article in website.articles if article.get_href() == href), None)
    
    @property
    def get_title(self):
        return self.__title

    @property
    def get_href(self):
        return self.__href

    @property
    def get_image(self):
        return self.__image

    @property
    def get_description(self):
        return self.__description

    @property
    def get_content(self):
        return self.__content

    @property
    def get_rating(self):
        return self.__rating

    def get_locations(self):
        if(isinstance(self.__locations, Location)):
            return [self.__locations]
        return self.__locations

    def to_dict(self):
        return {
            "title": self.__title,
            "href": self.__href,
            "image": self.__image,
            "description": self.__description,
            "content": self.__content,
            "rating": self.__rating,
            "locations": [location.to_dict() for location in self.__locations]
        }
    
website = Website()

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


    website.promotion.add_tour('1')

    Article.add_article("Exploring the Alps", "alps", "/Articleimage/japan.jpg", "A thrilling adventure in the Alps!", "Details about the journey through the Alps...", 4, Location("The Alps", "A mountain range in Europe"))
    Article.add_article("A Day in Paris", "paris", "/Articleimage/Paris.jpg", "Experience the beauty of Paris!", "A detailed guide to spending a day in Paris...", 5, Location("Paris", "The capital of France"))
    Article.add_article("Discovering Tokyo", "tokyo", "/Articleimage/Tokyo.jpg", "Explore the wonders of Tokyo!", "A comprehensive guide to Tokyo...", 4, Location("Tokyo", "The capital of Japan"))
    Article.add_article("Exploring the Alps", "alps", "/Articleimage/japan.jpg", "A thrilling adventure in the Alps!", "Details about the journey through the Alps...", 4, Location("The Alps", "A mountain range in Europe"))


create_enviroment()