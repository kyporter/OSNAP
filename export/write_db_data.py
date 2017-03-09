import export_data as exda
import sys

def main():
    if len(sys.argv)<2:
        print("Usage: python3 %s <directory_name>"%sys.argv[0])
        return

    dir_name = sys.argv[1]
    print("Files will be written to: %s"%dir_name)

    
