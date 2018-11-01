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
    #list = word_tokenize(string)
    list = string.split(' ')
    cleaned_list = []
    for item in list:
        cleaned_list.append(check_token(item))
    return ' '.join(cleaned_list)

def create_training_data(df):
    #shuffle the dataset and then split it for positive and nagative examples
    dictionary = df.to_dict(orient='index')
    keys = list(dictionary.keys())
    random.shuffle(keys)
    keys_neg = keys[:len(keys) // 2]
    keys_pos = keys[len(keys) // 2:]

    dict_pos = {}
    dict_neg = {}
    for i,  key in enumerate(keys_pos):
        dict_pos[i] = dictionary[key]
        dict_pos[i]['key'] = key
        dict_pos[i]['label'] = 'positive'

    #shuffle the responses of the responses to create negative examples
    suffled_keys_neg = keys[:len(keys) // 2]
    random.shuffle(suffled_keys_neg)
    for i,  key in enumerate(keys_neg):
        dict_neg[i] = {}
        dict_neg[i]['request'] = dictionary[key]['request']
        dict_neg[i]['response'] = dictionary[suffled_keys_neg[i]]['response']
        dict_neg[i]['key'] = key
        dict_neg[i]['label'] = 'negative'

    df_neg = pd.DataFrame.from_dict(dict_neg, orient='index')
    df_pos = pd.DataFrame.from_dict(dict_pos, orient='index')
    df = pd.concat([df_neg, df_pos])
    return df

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

    labled_df = create_training_data(df)
    labled_df.to_csv('RR_negative.csv')
if __name__ == '__main__':
    main()