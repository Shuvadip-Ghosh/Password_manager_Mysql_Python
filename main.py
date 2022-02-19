import logging
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
  options = [["See logs of previous activity"],
           ["Add a new password"],
           ["See a password"],
           ["Delete a password"],
           ["Update a username"],
           ["Update a password"],
           ["Update email or phone number"],
           ["See all password"],
           ["Generate a password"],
           ["Clear All previous activities."],
           ["Contact the developer"]]
  print("Type the code beside to do the following operations")
  print(tabulate(options,headers=["options"],tablefmt="psql",showindex="always"))  
def password_generator():
    while True:
        char = input("Please enter the Password length: ")
        if char.isdigit():
            break
        else:
            continue
    try:
        import string
        import random
        s1 = string.ascii_lowercase
        s2 = string.ascii_uppercase
        s3 = string.digits
        s = []
        s.extend(list(s1))
        s.extend(list(s2))
        s.extend(list(s3))
        plen = int(char)
        passw = "".join(random.sample(s, plen))
        return passw
    except:
        return "There was a problem generating the password"

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
    option = input("password manager# ")
    if option == "0":
        logFile = open("Activity.log","r")
        logData = logFile.readlines()
        logFile.close()
        # print(logData)
        for data in logData:
            ind = logData.index(data)
            sp = data.split(":-")
            sp[1] = sp[1].replace("\n","")
            logData[ind] = sp
        print(tabulate(logData, headers=["Time", "Message"],showindex="always",tablefmt="psql"))
    elif option =="1":
      try:
        username= input("Sir Enter the Username: ")
        email = input("Sir please enter the Email or the Phone Number for your account: ")
        site = input("Sir please enter the name of the site or the app: ")
        passwor = input("Sir please enter your Passowrd(type \"generate\" for automatically generating it.): ")
        if passwor == "generate":
            response = password_generator()
            if response == "There was a problem generating the password":
                print(response+" therefore not saved try again")
                logger.info(response+" therefore not saved try again")
            else:
                print("The generated password is: "+response)
                encoded = encryptt(response)
                res = master_checker()
                if res == 1:      
                    add_database(username,email,encoded,site)
                    print("\n**********************************\nNew password added to the database\n**********************************\n")
                    logger.info("New Passowrd Added")
                else:
                    print("""*********************************************************************\nYour Master Pasword Was Incorrect so the new password cannot be added\n*********************************************************************\n""")
                    logger.info("Failed Adding password as the master password was wrong")
        else:
            encoded = encryptt(passwor)
            res = master_checker()
            if res == 1:      
                add_database(username,email,encoded,site)
                print("\n**********************************\nNew password added to the database\n**********************************\n")
                logger.info("New Passowrd Added")
            else:
                print("""*********************************************************************\nYour Master Pasword Was Incorrect so the new password cannot be added\n*********************************************************************\n""")
                logger.info("Failed Adding password as the master password was wrong")

      except Exception as e:
        print("Sir there was an error")
        print(e)
        logger.info("There was a problem adding the password")
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
          logger.info(f"Showed a password for the site or app: {site}")
        else:
            print("*********")
            print("Try Again")
            print("*********")
            logger.info(f"Did not show password for the {site}")
      except Exception as e:
        print("Sir there was an error")
        print(e)
        logger.info("There was a problem showing the error")
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
            logger.info("A Password was removed")
        else:
            print("*************************************************************")
            print("Your master password was incorrect And therefore not removed.")
            print("*************************************************************")
            logger.info("Master password was incorrect therefore password not removed")
      except Exception as e:
        print("Sir there was an error")
        print(e)
        logger.info("There pas was a problem removing the error")
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
            logger.info(f"Username updated for the {site}")
        else:
            print("**************************************************************************")
            print("Your master password was incorrect and therefore username was not updated.")
            print("**************************************************************************")
            logger.info("Master password was incorrect as the username was not updated ")
      except Exception as e:
        print("Sir there was an error")
        print(e)
        logger.info("There was a problem updating the username")
        continue

    elif option == "5":
      try:
        site = input("Sir Please enter the site or the app name: ")
        username = input("Sir please enter the prevoiusly stored username for the new password(only for security purpose): ")
        email = input("Sir Please enter the Associated email or phonenumber: ")
        passw = input("Sir please enter your Passowrd(type \"generate\" for automatically generating it.): ") 
        if passw == "generate":
            response = password_generator()
            if response == "There was a problem generating the password":
                print(response+" therefore not saved try again")
                logger.info(response+" therefore not saved try again")
            else:
                res = master_checker()
                if res == 1:
                    passw = encryptt(response)
                    update_password(passw,username,site,email)
                    print("****************")
                    print("Password updated")
                    print("****************")
                    logger.info(f"Password updated for the {site}")
                else:
                    print("****************")
                    print("Master password was incorrect. Password not updated")
                    print("****************")
                    logger.info(f"Password not updated for {site}")
        else:
            res = master_checker()
            if res == 1:
                passw = encryptt(passw)
                update_password(passw,username,site,email)
                print("****************")
                print("Password updated")
                print("****************")
                logger.info(f"Password updated for the {site}")
            else:
                print("****************")
                print("Master password was incorrect. Password not updated")
                print("****************")
                logger.info(f"Password not updated for {site}")
      except Exception as e:
        print("Sir there was an error")
        print(e)
        logger.info("There was an error updating the password")
        continue

    elif option == "6":
      try:
        site = input("Sir Please enter the site or the app name: ")
        username = input("Sir please enter the prevoiusly stored username: ")
        emaill = input("Sir please entr the old email associated with the account: ")
        email = input("Sir please enter the new Email or Phone number: ")
        res = master_checker()
        if res == 1:
            update_email(email,username,site,emaill)
            print("*****************************")
            print("Email or Phone Number updated")
            print("*****************************")
            logger.info("Email or pone number Updated")
        else:
            print("*****************************")
            print("Email or Phone Number not updated")
            print("*****************************")
            logger.info("Master password incorrect therefore email or phone number not updated")
      except Exception as e:
        print("Sir there was an error")
        print(e)
        logger.info("There was an error updating the email or phone number")
        continue

    elif option == "7":
      try:
        res = master_checker()
        if res == 1:
          datas = get_all()
          passwords = []
          for data in datas:
            #print(data)
            passowrd = decryptt(data[2])
            passwords.append([data[0],data[1],passowrd, data[3]])
          print(tabulate(passwords, headers=["Username", "Email or Phone", "Password","Site or App"],showindex="always",tablefmt="psql"))
          logger.info("Displayed all the stored password")
      except Exception as e:
        print("Sir there was an error")
        print(e)
        logger.info("There was an error displaying all the password")
        continue

    elif option == "8":
        res = password_generator()
        if res == "There was a problem generating the password":
            print(res)
        else:
            print("Your Passowrd is: "+res)
        logger.info("Generated a new Password")
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
    logging.basicConfig(filename="Activity.log",format='%(asctime)s :- %(message)s',
                        filemode='a',datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info("Session Started")
    print_menu()
    main()
