import requests
import sys
import json

def main():
    if len(sys.argv)<4:
        print("Usage: python3 %s <URL> <username> <password>"%sys.argv[0])
        return

    routename = sys.argv[1] + 'update_user'
    uname = sys.argv[2]
    pword = sys.argv[3]

    r = requests.post(routename, data = {'update_type':'activate', 'username':uname, 'password':pword})
    
    print(r.text)


if __name__=='__main__':
    main()

