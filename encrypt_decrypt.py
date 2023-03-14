from cryptography.fernet import Fernet

key = Fernet.generate_key() # creating key
with open("my_key.key", "wb") as my_key:
    my_key.write(key)

'''ENCRYPTING''' # comment out code for decryption
# to re-use the key or use the key someone shared with us, comment out the above code and follow the code below

with open("my_key.key", "rb") as my_key:
    key = my_key.read()
print(key)  # key is loaded to our environment

f = Fernet(key)  # key is stored in variable f.

with open("text.txt", "rb") as original_file:
    original = original_file.read()

encrypted = f.encrypt(original)

with open("encrypted_text.txt", "wb") as encrypted_file:
    encrypted_file.write(encrypted)


'''DECRYPTING '''# comment out code for encryption
f = Fernet(key)  # key is stored in variable f.

with open("encrypted_text.txt", "rb") as encrypted_file:
    encrypted = encrypted_file.read()

decrypted = f.decrypt(encrypted)

with open("decrypted_text.txt", "wb") as decrypted_file: # writing into a new file
    decrypted_file.write(decrypted)

