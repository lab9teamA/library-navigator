
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
    def get_all_by_users(user_list):
        response = []
        for user in user_list:
            if user in locations.locmap:
                response.append(locations.locmap[user])
        return response

    @staticmethod
    def get_all_public_locations():
        return [loc for loc in locations.locmap.values() if not loc.private]
