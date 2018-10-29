import pandas as pd
import csv
from nltk import word_tokenize
import string as s
import re

def check_token(string):
    if string.isdigit() or string.isdecimal():
        string = '<num>'
    exclude = set(s.punctuation)- set(['<', '>'])
    string = ''.join(ch for ch in string if ch not in exclude)

    return string.lower()

def remove_links(string):
    if re.search('\{', string):
        new_string = ''
        parts = string.split('}}')
        for part in parts[:-1]:
            p = part.split('{')
            new_string = new_string + p[0] + '<link> '
        new_string = new_string + parts[-1]
        return new_string
    return string

def filter_sentence(string):
    string = remove_links(string)
    list = string.split(' ')
    cleaned_list = []
    for item in list:
        cleaned_list.append(check_token(item))
    return ' '.join(cleaned_list)

def main():
    filename = '/home/mattd/datasets/CarRepairData.csv'
    with open(filename, newline='') as csvfile:
        pairs = {}
        pair_count = 0
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"', )
        for row in csvreader:
            for i, element in enumerate(row):
                if (element != 'user'):
                    continue
                elif not re.search('\\\\', row[i + 1]):
                    pairs[pair_count] = {}
                    pairs[pair_count]['request'] = filter_sentence(row[i + 1])
                    pairs[pair_count]['response'] = filter_sentence(row[i + 3])
                    pair_count += 1
    df = pd.DataFrame.from_dict(pairs, orient='index')
    print('faggot')

if __name__ == '__main__':
    main()