from tkinter import *
from PIL import Image, ImageTk
from os import path
import json

import classes

top_bg = '#E50914'
bot_bg = '#B81D24'
bg = '#F5F5F1'

user = ''
tries = 0
user_object = ''
content_object = ''
step = 1


new_fname = ''
new_lname = ''
new_password = ''



win = Tk()
win.geometry('800x500')
win.config(bg='black')



def login():
    global user
    user = user_input.get()
    if user in classes.users.keys():
        print('username found')
        submit_button.config(command=password)
        input_lbl.config(text='Password: ')
        display_feedback('Please Enter your password, then hit submit')
        add_friend_entry.delete(0, END)

    else:
        print('username not found')
        display_feedback('It looks like you dont have an account with us. If you would like to create one, type the username you would like in the box and hit submit')
        # Username not found...\nEnter username and click submit\nagain to create an account
        submit_button.config(command=create_user)


def password():
    global user, tries
    print('handling password')

    if tries < 3:
        if classes.users[user]['_User__password'] == user_input.get():
            print('sucess')
            add_friend_entry.delete(0, END)
            change_button.config(state=NORMAL)
            objectify_current_user()
            friends_dashboard()
        else:
            display_feedback(f'Incorrect password, {3 - tries} attempts remaining')

        tries += 1
    else:
        display_feedback('Remember your password!')
        submit_button.config(state=DISABLED)



def create_user():
    global user, step, new_fname, new_lname, new_password
    selection = user_input.get()

    if step == 1:
        input_lbl.config(text='Username: ')
        if selection in classes.users.keys():
            display_feedback('Username has been taken. Try a new one')
            add_friend_entry.delete(0, END)
        else:
            input_lbl.config(text='First Name: ')
            user = selection
            display_feedback('Please enter your first name')
            step += 1
            add_friend_entry.delete(0, END)
    elif step == 2:
        input_lbl.config(text='Last Name: ')
        new_fname = selection
        print(f'users first name is {new_fname}')
        display_feedback('Please enter your last name')
        step += 1
        add_friend_entry.delete(0, END)
    elif step == 3:
        input_lbl.config(text='Password: ')
        new_lname = selection
        display_feedback('Please enter a password for your account. Be sure to remember it!')
        step += 1
        add_friend_entry.delete(0, END)
    elif step == 4:
        new_password = selection
        temp_object = classes.User(new_password, new_fname, new_lname)

        classes.users[user] = temp_object.__dict__

        print('Account Created')
        change_button.config(state=NORMAL)
        objectify_current_user()
        friends_dashboard()



def objectify_current_user():
    global user_object, user
    user_object = classes.User(
        classes.users[user]['_User__password'],
        classes.users[user]['_fname'],
        classes.users[user]['_lname'],
        classes.users[user]['friends'],
        classes.users[user]['ratings']
    )


def objectify_content():
    global content_object
    if 'seasons' in classes.content[content_index].keys():
        print('show')
        content_object = classes.Show(
            classes.content[content_index]['title'],
            classes.content[content_index]['year'],
            classes.content[content_index]['genre'],
            classes.content[content_index]['content_rating'],
            classes.content[content_index]['user_rating'],
            classes.content[content_index]['seasons']
        )
    else:
        print('movie')
        content_object = classes.Movie(
            classes.content[content_index]['title'],
            classes.content[content_index]['year'],
            classes.content[content_index]['genre'],
            classes.content[content_index]['content_rating'],
            classes.content[content_index]['user_rating'],
            classes.content[content_index]['length']
        )



def friends_dashboard():
    add_friend_entry.delete(0, END)
    list_lbl.config(text='content')
    change_button.config(text='View Content', command=content_dashboard)
    submit_button.config(command=add_friend)
    input_lbl.config(text='Username: ')
    listbox.bind('<<ListboxSelect>>', display_friend)
    listbox.delete(0, END)

    if len(user_object.friends) == 0:
        listbox.delete(0, END)
        display_feedback(f' Welcome {user_object.fname}! It looks like you havent friended anyone yet. To friend someone, type their username in the box and hit submit!')


        name_lbl.config(text=f'Hello {user_object.fname}!')
        interest1.config(text='Add Friends Below or click view content!')
        # interest2.config(text=f' Welcome {user_object.fname}! It looks like you havent friended anyone yet. To friend someone, type their username in the box and hit submit!')




    else:
        display_feedback(f' Welcome {user_object.fname}! browse around by selecting your friends names from the listbox, or enter usernames to add new friends!')
        interest1.config(text='Select a friend from your friends list to view their profile!')
        # interest2.config(text=f' Welcome {user_object.fname}! browse around by selecting your friends names from the listbox, or enter usernames to add new friends!')
        listbox.delete(0, END)
        for friend in user_object.friends:
            listbox.insert(END, friend)

    interests_lbl.config(text='')
    interest2.config(text='')
    interest3.config(text='')

    ratings_lbl.config(text='')
    rating1.config(text='')
    rating2.config(text='')
    rating3.config(text='')



def content_dashboard():
    add_friend_entry.delete(0, END)
    list_lbl.config(text='content')
    change_button.config(text='View Friends List', command=friends_dashboard)
    input_lbl.config(text='Rating: ')
    submit_button.config(command=rate_content)
    display_feedback('View content by clicking different movies or shows from the list. Rate your selected content by giving it a rating form 1-5, then click submit.')
    listbox.bind('<<ListboxSelect>>', display_content)
    listbox.delete(0, END)
    print('viewing content dashboard')

    for content in classes.content:
        listbox.insert(END, content['title'])

    name_lbl.config(text=f'Hello {user_object.fname}!')
    interests_lbl.config(text='')
    interest1.config(text='Here you are able to view content details, and rate content.\n Select a movie or show from the list to get started!')
    interest2.config(text='')
    interest3.config(text='')
    ratings_lbl.config(text='')
    rating1.config(text='')
    rating2.config(text='')
    rating3.config(text='')



def display_friend(event):
    print('displaying homie')
    friend_index = listbox.curselection()[0]
    friend_username = user_object.friends[friend_index]
    print(friend_username)

    name_lbl.config(text=f"{friend_username}'s Profile")

    interests_lbl.config(text='Similar Intrests')


    similar_interests = list()
    for uk, uv in user_object.ratings.items():
        print('users rating')
        print(f'{uk}    {uv}')
        for fk, fv in classes.users[friend_username]['ratings'].items():
            print('friends ratings')
            print(f'{fk}    {fv}')

            if uk == fk:
                value = uv - fv
                if value < 1 or value > -1:
                    print('similar')
                    similar_interests.append(fk)

    print(similar_interests)

    if len(similar_interests) == 0:
        interest1.config(text="Looks like you guys dont have any similar interests")
    elif len(similar_interests) == 1:
        interest1.config(text=f"{similar_interests[0]}")
        interest2.config(text=f"")
        interest3.config(text=f"")
    elif len(similar_interests) == 2:
        interest1.config(text=f"{similar_interests[0]}")
        interest2.config(text=f"{similar_interests[1]}")
        interest3.config(text=f"")
    else:
        interest1.config(text=f"{similar_interests[0]}")
        interest2.config(text=f"{similar_interests[1]}")
        interest3.config(text=f"{similar_interests[2]}")

    ratings_lbl.config(text=f"{friend_username}'s Ratings")

    ratings_list = list(classes.users[friend_username]['ratings'].items())
    print(ratings_list)

    if len(ratings_list) == 0:
        rating1.config(text=f"Looks Like {friend_username} hasn't rated any movies yet")
        rating2.config(text=f"")
        rating3.config(text=f"")
    elif len(ratings_list) == 1:
        rating1.config(text=f"{ratings_list[0][0]}: {ratings_list[0][1]}")
        rating2.config(text=f"")
        rating3.config(text=f"")
    elif len(ratings_list) == 2:
        rating1.config(text=f"{ratings_list[0][0]}: {ratings_list[0][1]}")
        rating2.config(text=f"{ratings_list[1][0]}: {ratings_list[1][1]}")
        rating3.config(text=f"")
    else:
        rating1.config(text=f"{ratings_list[0][0]}: {ratings_list[0][1]}")
        rating2.config(text=f"{ratings_list[1][0]}: {ratings_list[1][1]}")
        rating3.config(text=f"{ratings_list[2][0]}: {ratings_list[2][1]}")



def display_content(event):
    global content_index
    print('Displaying Content')
    content_index = listbox.curselection()[0]

    objectify_content()

    name_lbl.config(text=f"{content_object.title}")

    if len(content_object.user_rating) == 0:
        interests_lbl.config(text='Users have not yet rated this content')
    else:
        interests_lbl.config(text=f"Rating: {content_object.display_rating()}")

    interest1.config(text=f"Year: {content_object.year}")
    interest2.config(text=f"Genre: {content_object.genre}")
    interest3.config(text=f"Content Rating: {content_object.content_rating}")
    ratings_lbl.config(text='')

    cls = classes.Movie
    if isinstance(content_object, cls):
        rating1.config(text=f"Length: {content_object.length}")
    else:
        rating1.config(text=f"{content_object.seasons}")



def rate_content():

    rating_str = user_input.get()

    try:
        rating = float(rating_str)
        if rating > 5 or rating < 0:
            raise TypeError

    except ValueError:
        display_feedback('Enter a number for your rating!')

    except TypeError:
        display_feedback('Rating needs to be in between 0 and 5')
    else:
        display_feedback('Your rating was recieved!')


        if content_object.title in user_object.ratings.keys():
            print('already rated')
            user_object.rate_content(content_object.title, rating)
            save_content()
            save_user()
        else:
            content_object.add_rating(rating)
            user_object.rate_content(content_object.title, rating)
            save_content()
            save_user()
            add_friend_entry.delete(0, END)

        # print(content_object.__dict__)
        # print(user_object.__dict__)



def add_friend():
    friend_username = user_input.get()
    # if addfriend(username) returns true: update listbox and display sucess message
    option = user_object.toggle_friend(friend_username)
    print(option)
    if option == 1:
        display_feedback('Friend Added!')
    elif option == 2:
        display_feedback('Friend Removed')
    else:
        display_feedback('invalid username')
    print(user_object.friends)
    save_user()
    friends_dashboard()


def display_feedback(feedback=''):
    displayed = ''
    count = 0
    for char in feedback:
        displayed += char
        count += 1

        if count > 29 and char == ' ':
            displayed += '\n'
            count = 0
    print(displayed)
    feedback_lbl.config(text=displayed)




def save_user():
    print('saving Users')
    classes.users[user] = user_object.__dict__
    with open('users.json', 'w') as fp:
        json.dump(classes.users, fp)

def save_content():
    print('Saving content')
    print(content_object.title)
    for obj in classes.content:
        if obj['title'] == content_object.title:
            obj = content_object.__dict__
    print(classes.content)

    with open ('content.json', 'w') as fp:
        json.dump(classes.content, fp)



def close():
    win.destroy()



user_input = StringVar()



top_frame = Frame(win, width=800, height=350, bg=top_bg)
top_frame.pack(pady=10, padx=10)
top_frame.grid_propagate(0)

list_lbl = Label(top_frame, text='Friends List', bg=top_bg)
list_lbl.grid(row=0, column=0, pady=0, padx=30, sticky=SW)

listbox = Listbox(top_frame, width=30)
listbox.grid(row=1, column=0, rowspan=8, padx=30, sticky=N)
listbox.bind('<<ListboxSelect>>', display_friend)

name_lbl = Label(top_frame, text='Welcome!', font=('Arial', 25), bg=top_bg)
name_lbl.grid(row=0, column=1, pady=10, padx=30)

interests_lbl = Label(top_frame, text='', font=('Arial', 15), bg=top_bg)
interests_lbl.grid(row=1, column=1, ipady=10, sticky=NW)

interest1 = Label(top_frame, text='In this app, you will be able to see what Netflix content', bg=top_bg)
interest1.grid(row=2, column=1, sticky=W)

interest2 = Label(top_frame, text='your friends enjoy, rate content, and More!', bg=top_bg)
interest2.grid(row=3, column=1, sticky=W)

interest3 = Label(top_frame, text='Enter your Username Below to continue...', bg=top_bg)
interest3.grid(row=4, column=1, sticky=W)

ratings_lbl = Label(top_frame, text='', font=('Arial', 15), bg=top_bg)
ratings_lbl.grid(row=5, column=1, ipady=10, sticky=W)

rating1 = Label(top_frame, text='', bg=top_bg)
rating1.grid(row=6, column=1, sticky=W)

rating2 = Label(top_frame, text='', bg=top_bg)
rating2.grid(row=7, column=1, sticky=W)

rating3 = Label(top_frame, text='', bg=top_bg)
rating3.grid(row=8, column=1, sticky=W)


change_button = Button(top_frame, text='View Content', command=content_dashboard, highlightbackground=top_bg, state=DISABLED)
change_button.grid(row=9, column=1, pady=10, sticky=NW)





bot_frame = Frame(win, width=800, height=150, bg=bot_bg)
bot_frame.pack(pady=(0,10), padx=10)
bot_frame.grid_propagate(0)

input_lbl = Label(bot_frame, text='username:', bg=bot_bg)
input_lbl.grid(row=0, column=0, padx=(30,5), pady=(30,10))

add_friend_entry = Entry(bot_frame, textvariable=user_input)
add_friend_entry.grid(row=0, column=1, pady=(30,5))

submit_button = Button(bot_frame, text='submit', command=login, width=10, highlightbackground=bot_bg)
submit_button.grid(row=0, column=2, sticky=E, padx=5, pady=(30,5))

exit_button = Button(bot_frame, text='exit', command=close, width=10, highlightbackground=bot_bg)
exit_button.grid(row=1, column=2, sticky=NE, padx=5)

feedback_lbl = Label(bot_frame, text='Enter your username and click\n submit to get started.', bg=bot_bg, justify=LEFT)
# find the length of the text to be returned and add line breaks
feedback_lbl.grid(row=0, rowspan=2, column=3, padx=20, pady=20, sticky=NSEW)



canvas = Canvas(bot_frame, width=50, height=50, bg=bot_bg, highlightthickness=0)
canvas.grid(row=0,rowspan=3, column=4, padx=30, pady=35, sticky=NS)
logo = Image.open('netflix_logo.png')
logo = ImageTk.PhotoImage(logo)
canvas.create_image(25, 25, image=logo)



win.mainloop()