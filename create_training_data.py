import pandas as pd
import csv
from nltk import word_tokenize
import string as s
import re
import random

def check_token(string):

    exclude = set(s.punctuation)- set(['<', '>', '?', '.', ',', '!'])
    string = ''.join(ch for ch in string if ch not in exclude)

    if string.isdigit() or string.isdecimal():
        string = '<num>'

    return string.lower()

def remove_links(string):
    if re.search('\{', string):
        new_string = ''
        parts = string.split('}}')
        for part in parts[:-1]:
            p = part.split('{')
            new_string = new_string + p[0] + 'linktoken '
        new_string = new_string + parts[-1]
        return new_string
    return string

def filter_sentence(string):
    string = remove_links(string)
    list = word_tokenize(string)
    cleaned_list = []
    for item in list:
        cleaned_list.append(check_token(item))
    return ' '.join(cleaned_list)

def create_training_data(df):
    df.to_dict(orient='index')

def main():
    filename = '/home/mattd/datasets/CarRepairData.csv'
    with open(filename, newline='') as csvfile:
        pairs = {}
        filtered_pairs = {}
        pair_count = 0
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"', )
        for row in csvreader:
            for i, element in enumerate(row):
                if (element != 'user'):
                    continue
                elif row[i + 3] != "":
                    filtered_pairs[pair_count] = {}
                    pairs[pair_count] = {}

                    filtered_pairs[pair_count]['request'] = \
                        filter_sentence(row[i + 1])
                    filtered_pairs[pair_count]['response'] = \
                        filter_sentence(row[i + 3])
                    pairs[pair_count]['request'] = filter_sentence(row[i + 1])
                    pairs[pair_count]['response'] = filter_sentence(row[i + 3])
                    pair_count += 1
    df = pd.DataFrame.from_dict(filtered_pairs, orient='index')
    df.to_csv('RRall2.csv')
    labled_df = create_training_data(df)

if __name__ == '__main__':
    main()