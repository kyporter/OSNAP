import requests
import sys

def main():
    if len(sys.argv)<3:
        print("Usage: python3 %s <URL> <username>"%sys.argv[0])
        return

    routename = sys.argv[1] + 'update_user'
    uname = sys.argv[2]

    r = requests.post(routename, data ={'update_type':"revoke", 'username': uname})
    


if __name__=='__main__':
    main()

