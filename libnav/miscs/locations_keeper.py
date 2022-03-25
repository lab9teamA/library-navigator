
class location:
    def __init__(self ,x :int ,y: int, floor: int, user, private:bool):
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
    def remove(user):
        locations.locmap.pop(user)

    @staticmethod
    def get_all_by_users(user_list, floor):
        response = []
        for user in user_list:
            if user in locations.locmap:
                if locations.locmap[user].floor == floor:
                    response.append(locations.locmap[user])
        return response

    @staticmethod
    def get_all_public_locations(floor):
        return [loc for loc in locations.locmap.values() if loc.floor == floor and not loc.private]

    @staticmethod
    def get_business_of_floor(floor):
        return len([loc for loc in locations.locmap.values() if loc.floor == floor])
