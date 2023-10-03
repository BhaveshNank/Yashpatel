import os
temp = {}
class User:
    def __init__(self, id, name):
        self.id=id
        self.name=name
    def in_list(self, lst: list):
        for i in lst:
            if i.id == self.id:
                return True
        return False
class SocialNetwork:
    def __init__(self):
        self.users: dict[User, list[User]] = {}
        self.name_mode = None
    
    def add_user_from_line(self, line):
        data = line.split()
        user_name = data[0].strip()
        if self.name_mode == None:
            if user_name.isdigit():
                self.name_mode = True
            else:
                self.name_mode = False
        if user_name not in temp.keys():
            temp[user_name] = user_name if user_name.isdigit() else len(temp.keys())
        user_id = temp[user_name]
        user = User(user_id, user_name)
        if len(data)!=2:
            self.users[user] = []
            return
        friend_name = data[1].strip()
        if friend_name not in temp.keys():
            temp[friend_name] = friend_name if friend_name.isdigit() else len(temp.keys())
        friend_id = temp[friend_name]
        friend = User(friend_id, friend_name)
        for u in self.users.keys():
            if u.id == user.id:
                self.users[u].append(friend)
                break
        else:
            self.users[user] = [friend]
        user, friend = friend, user
        for u in self.users.keys():
            if u.id == user.id:
                self.users[u].append(friend)
                break
        else:
            self.users[user] = [friend]
    
    def display(self):
        for u, f in self.users.items():
            print(f"{u.name} -> {', '.join(map(lambda x: x.name, f))}")
    
    def get_user_from_id(self, id: str) -> User:
        for u, f in self.users.items():
            if u.id == id:
                return u
        return None
    
    def get_user_from_input(self):
        text = "Enter user name: " if not self.name_mode else f"Enter user id as an integer from 0 to {len(self.users.keys())-1}: "
        ans = input(text)
        for u in self.users.keys():
            if not self.name_mode and u.name.lower() == ans.lower():
                return u
            if u.id == ans:
                return u
        print("User doesn't exist")
        return self.get_user_from_input()
def main():
    filename = input("Enter Filename:")
    if not filename: return
    if not os.path.exists(filename):
        print("File not found!!")
        return
    f = open(filename, "r")
    f_data = f.readlines()
    total_users = int(f_data[0].strip())
    f_data.pop(0)
    social_nw = SocialNetwork()
    for i in f_data:
        social_nw.add_user_from_line(i)
    temp = {}
    if input("Display the social network (y/n)?: ").lower() in ("y","yes"):
        social_nw.display()
    to_recommend_friend = True
    while to_recommend_friend:
        user = social_nw.get_user_from_input()
        found_ref = False
        existing_friend = social_nw.users[user]
        for i in existing_friend:
            suggestion = social_nw.users[social_nw.get_user_from_id(i.id)]
            if suggestion and not found_ref:
                for r in suggestion:
                    if i.id != r.id and user.id != r.id and not found_ref and not r.in_list(existing_friend):
                        found_ref = True
                        print(f"The recommended friend for {user.name} is {r.name}")
                        break
                if not found_ref:
                    for r in suggestion:
                        sub_suggestion = social_nw.users[social_nw.get_user_from_id(r.id)]
                        for s in sub_suggestion:
                            if i.id != s.id and user.id != s.id and not found_ref and not s.in_list(existing_friend):
                                found_ref = True
                                print("The recommended friend for %s is %s"%(user.name,s))
                                break
        if not found_ref:
            print("There is no recommended friend.")
        if input("Do you want to recommend friends to another user (y/n)? ").lower() in ("y","yes"):
            to_recommend_friend = True
        else:
            to_recommend_friend = False
    if input("Display how many friends a user has (y/n)?").lower() in ("y","yes"):
        user = social_nw.get_user_from_input()
        existing_friend = social_nw.users[social_nw.get_user_from_id(user.id)]
        if existing_friend:
            print(f"User {user.name} has {len(existing_friend)} friends")
    if input("Display the users with the least number of or have 0 friends (y/n)?").lower() in ("y","yes"):
        atleast_friend = []
        no_friend=  []
        for user, friend in social_nw.users.items():
            if len(friend) == 1 and not user.in_list(atleast_friend):
                atleast_friend.append(user)
            elif not friend and not user.in_list(no_friend):
                no_friend.append(user)
            for i in friend:
                usr_data = social_nw.users[social_nw.get_user_from_id(i.id)]
                if not usr_data and not i.in_list(no_friend):
                    no_friend.append(i.name)
        if atleast_friend:
            print(f"The user ID for the user with least friends is: {', '.join(map(lambda x: x.name, atleast_friend))}")
        if no_friend:
            print(f"The user ID for the user with 0 friends is: {', '.join(map(lambda x: x.name, no_friend))}")
    if input("Display the friends of the friends of a given user (y/n)?").lower() in ("y","yes"):
        user = social_nw.get_user_from_input()
        friends = social_nw.users[user]
        for u, friend in social_nw.users.items():
            if u.id != user.id and u.in_list(friends):
                common_list = set(friends).intersection(friend)
                mutual_frd = "None"
                if common_list:
                    mutual_frd = ",".join(map(lambda x: x.name, common_list))
                print("%s -> %s"%(u.name,mutual_frd))
    if input("Do you want to try another social network (y/n)?").lower() in ("y","yes"):
        return main()
main()