import sys
import json

def main():
    json_file = sys.argv[1]
    with open(json_file, 'r') as file:
        test_results = json.load(file)
        print(f"Test Results: {test_results}")

if __name__ == "__main__":
    main()