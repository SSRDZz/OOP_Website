class website:
    def __init__(self):
        self.__user = []
        self.__tour_manager = ''

    def search_user(self,user_id):
        pass

    def search_tour(self,tour_id): #ต้องใช้ใน search.py
        return self.__tour_manager.search_tour(tour_id)
    
    def booking_tour(self, user, tour_program, data):
        return user.create_booking_tour(tour_program, data)


class Booking:
    def __init__(self,tour_program, data):
        self.__tour_program = tour_program
        self.__data = data


class User:
    def __init__(self):
        self.__booking = []

    def create_booking_tour(self,tour_program, data):
        try:
            # สร้าง booking ตามเงื่อนไขสักอย่าง bogo = Booking(tour_program, datatour_program, data)
            pass
  
            self.__booking.append(Booking)
            return True
        
        except : 
            return False


class TourManager:
    def __init__(self):
        self.__tour_program = []
    def search_tour(tour_id): #ต้องใช้ใน search.py
        pass
