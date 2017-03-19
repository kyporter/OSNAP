import requests
import sys

role_dict = {"LO" : "Logistics Officer", "FO" : "Facilities Officer"}

def main():
    if len(sys.argv)<5:
        print("Usage: python3 %s <URL> <username> <password> <role: LO or FO>"%sys.argv[0])
        return
    if sys.argv[4].upper() != "LO" and sys.argv[4].upper() != "FO":
        print("invalid role, please enter LO or FO as role")

    routename = sys.argv[1] + 'update_user'
    uname = sys.argv[2]
    pword = sys.argv[3]
    role_abb = sys.argv[4]
    role = role_dict[role_abb]

    r = requests.post(routename, data = {'update_type':'activate', 'username':uname, 'password':pword, 'role':role})
    

if __name__=='__main__':
    main()

