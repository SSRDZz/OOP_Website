class Website:
    def __init__(self):
        self.__tour_manager = ''
    
    def search_tour(self,id,place,time):
        return self.__tour_manager.search_tour(id,place,time)
    

class TourManager:
    def __init__(self):
        self.__tour_program = []


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

