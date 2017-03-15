import
import sys
import json

def main():
    if len(sys.argv)<3:
        print("Usage: python3 %s <URL> <username>"%sys.argv[0])
        return

    routename = sys.argv[1]
    uname = sys.argv[2]

    arguments = jsonify(update_type = "revoke", username = uname)
    
    return


if __name__='__main__':
    main()

