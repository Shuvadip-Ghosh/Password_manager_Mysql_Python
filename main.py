import mysql.connector
import hashlib
from getpass import getpass
import os
from tabulate import tabulate
from cryptography.fernet import Fernet
from cffi import FFI
ffi = FFI()

master_hash = 'f43611020baaca84c6f4a2c57b9cca9a'

def master_checker():
    password = getpass("Enter the master password : ")
    h = hashlib.md5(password.encode())
    hash = h.hexdigest()
    if hash == master_hash:
        return 1
    else:
        return 0
    

def add_database(username,email,passw,site):
  cur.execute(
  f"""INSERT INTO tech (username,email,passw,site)
  VALUES 
  ('{username}', '{email}', '{passw}', '{site}')""")
  conn.commit()
def get_all():
  cur.execute("SELECT * FROM tech")
  # A1fy5r0x
  return cur.fetchall()
def get_site(site):
  cur.execute("SELECT * FROM tech WHERE site=%(site)s",{'site':site})
  return cur.fetchall()
def remove(username,site,email): 
    cur.execute(f"DELETE from tech WHERE username = %(username)s AND site =%(site)s AND email = %(email)s",{'username':username,'site':site,'email':email}) 
    conn.commit()
def update_username(username,site,emaill):
  cur.execute(f"""UPDATE tech SET username = '{username}'                     
                WHERE site = '{site}' AND email = '{emaill}'""")
  conn.commit()
def update_password(password,username,site,emaill):
  cur.execute(f"""UPDATE tech SET passw = '{password}'                     
                WHERE site = '{site}' AND username = '{username}' AND email = '{emaill}'""")
  conn.commit()
def update_email(email,username,site,emaill):
  cur.execute(f"""UPDATE tech SET email = '{email}'                     
                WHERE site = '{site}' AND username = '{username}' AND email = '{emaill}'""")
  conn.commit()

def print_menu():
  options = [["1","Add a new password"],["2","See a password"],["3","Delete a password"],["4","Update a username"],
             ["5","Update a password"],["6","Update email or phone number"],["7","See all password"],
             ["8","Generate a password"],["9","Clear All previous activities."],["10","Contact the developer"]]
  print("Type the code beside to do the following operations")
  print(tabulate(options,headers=["code","options"],tablefmt="psql"))  
def password_generator(plen):
    import string
    import random
    s1 = string.ascii_lowercase
    s2 = string.ascii_uppercase
    s3 = string.digits
    s = []
    s.extend(list(s1))
    s.extend(list(s2))
    s.extend(list(s3))
    plen = int(plen)
    passw = "".join(random.sample(s, plen))
    print("Your password is: "+passw)

def encryptt(password):
    f = Fernet(key)
    password = password.encode()
    token = f.encrypt(password)
    #print(type(token))
    token = token.decode()
    return token   
def decryptt(token):
    f = Fernet(key)
    token = token.encode()
    passowrd = f.decrypt(token)
    return passowrd.decode()
def main():
  while True:
    option = input("password_manager# ")
    if option =="1":
      try:
        username= input("Sir Enter the Username: ")
        passwor = input("Sir please enter your Passowrd: ")
        encoded = encryptt(passwor)
        email = input("Sir please enter the Email or the Phone Number for your account: ")
        site = input("Sir please enter the name of the site or the app: ")
        res = master_checker()
        if res == 1:      
            add_database(username,email,encoded,site)
            print("\n**********************************\nNew password added to the database\n**********************************\n")
        else:
            print("""*********************************************************************\nYour Master Pasword Was Incorrect so the new password cannot be added\n*********************************************************************\n""")
      except Exception as e:
        print("Sir there was an error")
        print(e)
        continue

    elif option == "2":
      try:
        site = input("Sir please enter the site or the name of the app to see the password: ")
        password = getpass("Enter the master password : ")
        h = hashlib.md5(password.encode())
        hash = h.hexdigest()
        if hash == master_hash:
          passwords = []
          datas = get_site(site)
          for data in datas:
            #print(data)
            passowrd = decryptt(data[2])
            passwords.append([data[0],data[1],passowrd, data[3]])
          print(tabulate(passwords, headers=["Username", "Email or Phone", "Password","Site or App"],showindex="always",tablefmt="psql"))
        else:
            print("*********")
            print("Try Again")
            print("*********")
      except Exception as e:
        print("Sir there was an error")
        print(e)
        continue

    elif option == "3":
      try:
        username = input("Sir Enter the Username for the stored password: ")
        site = input("Sir please enter the name of the site or the app: ")
        email = input("Sir Please enter the associated email or phonenumber: ")
        res = master_checker()
        if res == 1: 
            remove(username,site,email)
            print("****************")
            print("Password removed")
            print("****************")
        else:
            print("*************************************************************")
            print("Your master password was incorrect And therefore not removed.")
            print("*************************************************************")
      except Exception as e:
        print("Sir there was an error")
        print(e)
        continue


    elif option == "4":
      try:
        username = input("Sir please enter the new Useranme: ")
        site = input("Sir please input the site or app for the new username: ")
        email = input("Sir please input the Asociated email or phonenumber: ")
        res = master_checker()
        if res == 1: 
            update_username(username,site,email)
            print("****************")
            print("Username Updated")
            print("****************")
        else:
            print("*************************************************************")
            print("Your master password was incorrect and therefore not removed.")
            print("*************************************************************")
      except Exception as e:
        print("Sir there was an error")
        print(e)
        continue

    elif option == "5":
      try:
        site = input("Sir Please enter the site or the app name: ")
        username = input("Sir please enter the prevoiusly stored username for the new password(only for security purpose): ")
        email = input("Sir Please enter the Associated email or phonenumber: ")
        passw = input("Sir please enter the new passowrd: ")  
        passw = encryptt(passw)
        update_password(passw,username,site,email)
        print("****************")
        print("Password updated")
        print("****************")
      except Exception as e:
        print("Sir there was an error")
        print(e)
        continue

    elif option == "6":
      try:
        site = input("Sir Please enter the site or the app name: ")
        username = input("Sir please enter the prevoiusly stored username: ")
        emaill = input("Sir please entr the old email associated with the account: ")
        email = input("Sir please enter the new Email or Phone number: ")
        update_email(email,username,site,emaill)
        print("*****************************")
        print("Email or Phone Number updated")
        print("*****************************")
      except Exception as e:
        print("Sir there was an error")
        print(e)
        continue

    elif option == "7":
      try:
        password = getpass("Enter the master password : ")
        h = hashlib.md5(password.encode())
        hash = h.hexdigest()
        if hash == master_hash:
          datas = get_all()
          passwords = []
          for data in datas:
            #print(data)
            passowrd = decryptt(data[2])
            passwords.append([data[0],data[1],passowrd, data[3]])
          print(tabulate(passwords, headers=["Username", "Email or Phone", "Password","Site or App"],showindex="always",tablefmt="psql"))
      except Exception as e:
        print("Sir there was an error")
        print(e)
        continue

    elif option == "8":
      char = input("Please enter the Password length in integers: ")
      password_generator(char)
    elif option == "9": 
      if os.name == "posix":
          os.system("clear")	
      else:
          os.system("cls")
      print_menu()
    elif option == "10":
      print("Name : Shuvadip Ghosh")
      print("Email : shuvadipdeveloper@gmail.com")
      print("Please feel free to contact Mr Shuvadip Ghosh For any suggestions or any issues.")



if __name__ == "__main__":
  res = master_checker()
  if res == 1:
    conn = mysql.connector.connect(
      host="mysql-host",
      user="mysql-user",
      password="mysql-passowrd",
      database="mysql-database"
    )
    file = open("key.txt","rb")
    key = file.read()
    file.close()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tech (
      username text NOT NULL,
      email text NOT NULL,
      passw text NOT NULL,
      site text NOT NULL
    )
    """)
    print_menu()
    main()
