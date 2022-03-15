
class location:
    def __init__(self ,x :int ,y: int, floor: int, user: int, private:bool):
        self.x = x
        self.y = y
        self.floor = floor
        self.user = user
        self.private = private


class locations:
    __locmap = dict()

    def add(self, loc: location):
        self.__locmap[location.user] = loc

    def remove(self, loc: location):
        self.__locmap.pop(loc)

    def get_all_by_users(self, user_list: list):
        response = []
        for user in user_list:
            if user in self.__locmap:
                response.append(self.__locmap[user])
        return response

    def get_all_public_locations(self):
        return [x for x in self.__locmap.items() if not x.private]
