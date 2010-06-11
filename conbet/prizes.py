# -*- coding: utf-8 -*-
import math

class WorldCup2010Prizes:
    """
    Prizes for the World Cup 2010.

    """
    def __init__(self, bet_price):
        self.bet_price = bet_price

    def set_prizes(self, users):
        """
        users attribute must contain a position attribute

        """   
        total_prizes = len(users) * self.bet_price
        
        # Definition of available prizes
        last = float(self.bet_price)
        third  = float(math.floor(((total_prizes - last)*0.05)))
        second = float(math.floor(((total_prizes - last)*0.25)))
        first = float(total_prizes - second - third*3 - last)

        self.available_prizes = [third, third, third, second, first]
        position = 1
        firsts = filter(lambda x: x["position"]==position, users)
        
        self.set_prize(firsts,  "first")
        if len(firsts)==1:
            position += 1
            seconds = filter(lambda x: x["position"]==position, users)
            self.set_prize(seconds, "second")
        position += 1
        self.set_prize(self.get_thirds(users, position),  "third")

        position = users[len(users)-1]["position"]
        last_users = []
        for i in range(len(users)-1, -1, -1):
            if users[i]["position"] == position:
                last_users.append(users[i])
            else:
                break

        for user in last_users:
            if not ("prize" in user):
                user["prize"] = 0 
            user["prize"] += last / len(last_users)
            user["class_name"] = "last"

    def get_thirds(self, users, initial_pos):
        position = initial_pos
        thirds = []
        if (len(users)>=len(self.available_prizes)):
            while len(thirds) < len(self.available_prizes):
                thirds += filter(lambda x: x["position"]==position, users)
                position += 1
        return thirds

    def set_prize(self, users, class_name):
        real_prize = 0
        if len(self.available_prizes) > 0:
            for i in range(0,min(len(users), len(self.available_prizes))):
                real_prize += self.available_prizes.pop()
            for user in users:
                user["prize"] = real_prize / len(users)
                user["class_name"] = class_name
