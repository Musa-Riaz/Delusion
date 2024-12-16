# this creates a copy of the original dataset's first n rows for testing
import csv

NUM_ARTICLES = 1000
with open('medium_articles.csv', encoding='utf-8') as file:
    reader = csv.reader(file)
    with open('n_articles.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in range(NUM_ARTICLES):
            this_row = next(reader)
            writer.writerow(this_row)
