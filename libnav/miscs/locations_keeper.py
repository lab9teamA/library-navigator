
class location:
    def __init__(self ,x :int ,y: int, floor: int, user: int, private:bool):
        self.x = x
        self.y = y
        self.floor = floor
        self.user = user
        self.private = private


class locations:
    locmap = dict()

    @staticmethod
    def add(loc: location):
        locations.locmap[loc.user] = loc

    @staticmethod
    def remove(loc: location):
        locations.locmap.pop(loc)

    @staticmethod
    def get_all_by_users(user_list, floor):
        response = []
        for user in user_list:
            if user in locations.locmap:
                response.append(locations.locmap[user])
        response = [{"x": loc.x, "y": loc.y, "private": loc.private} for loc in response if loc.floor == floor]
        return response

    @staticmethod
    def get_all_public_locations(floor):
        return [{"x": loc.x, "y": loc.y} for loc in locations.locmap.values() if loc.floor == floor and not loc.private]

    @staticmethod
    def get_business_of_floor(floor):
        return len([loc for loc in locations.locmap.values() if loc.floor == floor])
