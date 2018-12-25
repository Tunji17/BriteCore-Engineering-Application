# import fernet from cryptography
from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?

message = b'gAAAAABcIJiowp3R-qqNZaR4VCPmHe8L7_MvQDRtwl_foT4_m9taAZ0nQcQZD9xQ2fkLwGSA4d57aCVuOOn5x5VmqzavJnpSr1y_P7r_ZyV9-tYO3hMPGpqryxKD2Mp5JwgnU59E_uw0F-4STcYmSHMPi5a-5IuMwhmDc8cCrm_OjBE1egv47NB7FsS0UtQdo6vGCy7h7e8E'

def main():
    f = Fernet(key)
    print(f.decrypt(message))

if __name__ == "__main__":
    main()



# result = b'https://engineering-application.britecore.com/e/t24e118s11t/ImplementationEngineer'
