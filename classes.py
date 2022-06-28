import json
from os import path
import statistics




global users
# users = {'jawilco1': {'_User__password': 'jaw898', '_fname': 'Jake', '_lname': 'Wilcox', 'friends': [], 'ratings': {}},
#          'kabeyta1': {'_User__password': 'k', '_fname': 'Kaya', '_lname': 'Abeyta', 'friends': ['jawilco1'], 'ratings': {}}
#          }

users = dict()
content = list()



class User:

    def __init__(self, password='', fname='', lname='', friends=None, ratings=None):
        self.__password = password
        self.fname = fname
        self.lname = lname
        if friends is None:
            self.friends = list()
        else:
            self.friends = friends

        if ratings is None:
            self.ratings = dict()
        else:
            self.ratings = ratings


    @property
    def fname(self):
        return self._fname

    @fname.setter
    def fname(self, fn):
        print('setting')
        inital = fn[0].upper()
        rest = fn[1:].lower()
        name = (f'{inital}{rest}')
        self._fname = name

    @property
    def lname(self):
        return self._lname

    @lname.setter
    def lname(self, ln):
        print('setting')
        inital = ln[0].upper()
        rest = ln[1:].lower()
        name = (f'{inital}{rest}')
        self._lname = name

    def toggle_friend(self, user):

        if user in users.keys():
            if user not in self.friends:
                self.friends.append(user)
                return 1
            else:
                self.friends.remove(user)
                return 2
        else:
            return 3


    def rate_content(self, content='', rating=0.0):
        self.ratings[content] = rating



class Content:

    def __init__(self, title='', year=0, genre='', content_rating='', user_rating=None):
        self.title = title
        self.year = year
        self.genre = genre
        self.content_rating = content_rating

        if user_rating is None:
            self.user_rating = list()
        else:
            self.user_rating = user_rating


    def display_rating(self):
        rating = statistics.mean(self.user_rating)
        return f'{rating:.2f}'


    def add_rating(self, new_rating):
        self.user_rating.append(new_rating)
        #do exception handeling in the GUI file so we can display user feedback

class Movie(Content):

    def __init__(self, title, year, genre, content_rating, user_rating, length):
        super().__init__(title, year, genre, content_rating, user_rating)
        self.length = length

class Show(Content):

    def __init__(self, title, year, genre, content_rating, user_rating, seasons):
        super().__init__(title, year, genre, content_rating, user_rating)
        self.seasons = seasons



# json files


with open('users.json') as fp:
    users = json.loads(fp.read())
    print(users)

with open('content.json') as fp:
    content = json.loads(fp.read())




# if not path.isfile('users.json'):
#     print('creating file')
#     with open('users.json', 'w') as fp:
#         json.dump(users, fp)



# def save_content():
#     with open('content.json', 'w') as fp:
#         json.dump(content, fp)
#
#
# with open('content.json') as fp:
#     content = json.loads(fp.read())
#
#
# content1 = Show('Test', 200, 'Comedy', 'TV-PG', [], '3 Seasons')
# content.append(content1.__dict__)
# save_content()
#
#
#
#
# print(content1.__dict__)
# content1.add_rating(5)
# content1.add_rating(0)
# print(content1.display_rating())



# username = input('enter your username: ')
# password = input('Enter your password: ')
# users[username] = User(password, 'JaKE', 'wilcox').__dict__
# print(users)
#
#
#
# user2 = User('k', 'kaya', 'abeyta', ['jawilco1'])
# #user2.add_friends('jawilco1')
#
#
# print(user2.__dict__)
#
# user3 = User('fdsa', 'fuzzy', 'f', ['jawilco1'])
#
# user3.add_friends('kabeyta1')
# print(user3.__dict__)





