# import fernet from cryptography
from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?

message = b'gAAAAABcPadEyTBcV4h_rAGRHydOxR5RJAcddbeNksaS5eLJeqhlbTDFRenO7y7IeQHbQhuMbcagVhHAaHj4Hw4y-M1YiILv14Tds4H45Cjq608fcqKUNHbUqrCvpBIiU6YvOqhnjed8625NLAxpb5qmS50GnqW7sZQf2f-b8MT62ZP_6D2CFkNVpnAMhz3ND3MHxjWMzk8_'

def main():
    f = Fernet(key)
    print(f.decrypt(message))

if __name__ == "__main__":
    main()



# result = b'https://engineering-application.britecore.com/e/t15e119s0t/ImplementationEngineer'
