import json

def read_data(filename):
    """Read the json data from file and return a dictionary."""
    with open(filename, 'rt') as file:
        data = file.read()
        dictionary_data = json.loads(data)
        return dictionary_data

def sum_data(data):
    total = 0
    for n in data:
        total += n
    return total

def main():
    dictionary_data = read_data('problem4.2.json')
    total = sum_data(dictionary_data['numbers'])
    print(total)

if __name__ == '__main__':
    main()