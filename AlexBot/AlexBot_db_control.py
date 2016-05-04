import pickle
import os

def init_db():
    file = open('simple_command.db', 'rb+')
    simple_command = pickle.load(file)
    file.close()
    return simple_command

def main():
    base=init_db()
    while(True):
        os.system('cls')
        print("1. Delete")
        print("2. Add")
        print("3. Show")
        print("4. Exit")
        choice=input()
        if(choice == "1"):
            print("Enter key: ")
            key = input()
            base.pop(key)
            file = open('simple_command.db', 'wb')
            pickle.dump(base, file)
            file.close()
            continue
        if(choice == "2"):
            print("Enter key: ")
            key=input()
            print("Enter command: ")
            base[key]=input()
            file = open('simple_command.db', 'wb')
            pickle.dump(base, file)
            file.close()
            continue
        if(choice == "3"):
            for key in base:
                print(key)
            input()
            continue
        if(choice == "4"):
            exit()
        os.system('cls')



main()