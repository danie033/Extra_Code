from pwdlib import PasswordHash

pass_hasher=PasswordHash.recommended()

plain_password="secret"
pass_hashed=pass_hasher.hash(plain_password)

print(f"Plain password: {plain_password}\n Hashed Password: {pass_hashed}") 