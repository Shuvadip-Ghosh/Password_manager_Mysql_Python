# Password_manager_Mysql_Python


The Deafult passowrd  = 6AMWeLb
and enter the required details around lines 10 to 15 and 
generate a key using the cryptography module using the following code 
The code below will generate a key and and save it in a text file
(Please run the code once before you start using using the passward manger or 
else the key in the text file will be replaced and you will not be able to decrypt your previously saved password if any.)

from cryptography.fernet import Fernet
key = Fernet.generate_key()
file = open('key.key', 'wb')  # Open the file as wb to write bytes
file.write(key)  # The key is type bytes still
file.close()

you will be good to go.
