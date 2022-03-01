from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import os
import pymongo
from re import search
import time


### connect to database ###

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["search_engine"]

mycol = mydb["inverted_index"]

### parse and indexing ###

def generate_html_url():
    path = 'C:\\Users\\Click\\Desktop\\DataSetFor IR BS'

    folders = os.listdir(path)
    files = []
    for i in folders:
        for j in os.listdir(f'{path}\\{i}'):
            files.append(i + '\\' + j)

    counter = 0
    cnt = 0
    for file in files:
        tree = ET.parse(f'C:\\Users\\Click\\Desktop\\DataSetFor IR BS\\{file}')
        root = tree.getroot()

        for html in root.iter('HTML'):
            with open(f'C:\\Users\\Click\\PycharmProjects\\search engine\\html files\\html-{counter}.html', 'w',
                      encoding='utf-8') as f:
                f.write(html.text)
            counter += 1

        for url in root.iter('URL'):
            with open(f'C:\\Users\\Click\\PycharmProjects\\search engine\\url files\\url-{cnt}.txt', 'w',
                      encoding='utf-8') as f:
                f.write(url.text)
            cnt += 1


def generate_body_title():
    path = 'C:\\Users\\Click\\PycharmProjects\\search engine\\html files'

    files = os.listdir(path)
    for file in range(len(files)):
        with open(f'{path}\\html-{file}.html', 'r', encoding='utf-8') as f:
            data = f.read()
            soup = BeautifulSoup(data, "html.parser")
            try:
                with open(f'C:\\Users\\Click\\PycharmProjects\\search engine\\title files\\title-{file}.txt', 'w',
                          encoding='utf-8') as titleFile:
                    titleFile.write(soup.title.text)
            except:
                pass

            try:
                with open(f'C:\\Users\\Click\\PycharmProjects\\search engine\\body files\\body-{file}.txt', 'w',
                          encoding='utf-8') as body:
                    body.write(soup.body.text)
            except:
                pass


inverted_index = {}


def invert_index():
    global inverted_index
    path = 'C:\\Users\\Click\\PycharmProjects\\search engine\\combine files'
    files = os.listdir(path)
    for name in range(len(files)):
        with open(f'{path}\\combine-{name}.txt', 'r', encoding='utf8') as file:
            read = file.read()

        data = read.split(' /**********/ ')
        title = data[1]
        body = data[2]
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~|،«»؛●'''
        for ele in title:
            if ele in punc:
                title = title.replace(ele, " ")

        for ele in body:
            if ele in punc:
                body = body.replace(ele, " ")

        body = body.split(' ')
        title = title.split(' ')
        id = str(name)
        for word in body:
            if word in ['', ' ', '  ', '   ', '    ']:
                continue
            word = word.strip()
            if word not in inverted_index.keys():
                inverted_index.update({word: [id]})
            elif id in inverted_index[word]:
                continue
            elif word in inverted_index.keys():
                inverted_index[word].append(id)

        for word in title:
            if word == '' or word == ' ' or word == '  ':
                continue
            word = word.strip()
            if word not in inverted_index.keys():
                inverted_index.update({word: [id]})
            elif id in inverted_index[word]:
                continue
            elif word in inverted_index.keys():
                inverted_index[word].append(id)


def merge_docs():
    path = 'C:\\Users\\Click\\PycharmProjects\\search engine\\body files'
    for i in range(len(os.listdir(path))):
        with open(f'''C:\\Users\\Click\\PycharmProjects\\search engine\\body files\\body-{i}.txt''', 'r',
                  encoding='utf-8') as f:
            body = f.read()
            body = body.replace('http:// www.Tebyan-Zn.ir', '').strip()
        with open(f'''C:\\Users\\Click\\PycharmProjects\\search engine\\title files\\title-{i}.txt''', 'r',
                  encoding='utf-8') as f:
            title = f.read()
        with open(f'''C:\\Users\\Click\\PycharmProjects\\search engine\\url files\\url-{i}.txt''', 'r',
                  encoding='utf-8') as f:
            url = f.read()

        with open(f'''C:\\Users\\Click\\PycharmProjects\\search engine\\combine files\\combine-{i}.txt''', 'w',
                  encoding='utf-8') as f:
            f.write(url + ' /**********/ ' + title + ' /**********/ ' + body)


### search and rank ###



path = 'C:\\Users\\Click\\PycharmProjects\\search engine\\combine files'
files = os.listdir(path)
read_files = []

for name in range(len(files)):
    with open(f'''{path}\\{'combine'}-{name}.txt''', 'r',
              encoding='utf-8') as f:
        read_files.append(f.read())


def AND_result(query):
    union = []
    ischeck = False

    words = query.split(' ')

    for word in words:
        dbSearch = mycol.find({'word': word})
        try:
            ids = str(dbSearch[0]['index']).split(", ")
        except:
            continue
        if len(union) == 0 and not ischeck:
            union = ids
            len(union)
            ischeck = True
            continue
        if len(union) == 0 and ischeck:
            break
        union = list(set(union).intersection(set(ids)))
    return union


def OR_result(query):
    combine = []

    words = query.split(' ')
    for word in words:
        dbSearch = mycol.find({'word': word})
        try:
            ids = str(dbSearch[0]['index']).split(", ")
            combine.extend(ids)
        except:
            continue
    return list(set(combine))


def NOT_result(query):
    result = []
    ischeck = False

    words = query.split(' ')

    for word in words:
        dbSearch = mycol.find({'word': word})
        try:
            ids = str(dbSearch[0]['index']).split(", ")
        except:
            continue
        if len(result) == 0 and not ischeck:
            result = ids
            ischeck = True
            continue
        if len(result) == 0 and ischeck:
            break
        result = [x for x in result if x not in ids]
    return result


def search_query(query):
    start_time = time.time()
    if search('AND', query):
        text = query.replace('AND ', '')
        return ranking(AND_result(text), query), (time.time() - start_time)
    elif search('OR', query):
        text = query.replace('OR ', '')
        return ranking(OR_result(text), query), (time.time() - start_time)
    elif search('NOT', query):
        text = query.replace('NOT ', '')
        return ranking(NOT_result(text), query), (time.time() - start_time)

    and_result = AND_result(query)
    ranked_and = ranking(and_result, query)
    or_result = OR_result(query)
    ranked_or = ranking(or_result, query)

    ranked_and['index'].extend(ranked_or['index'])
    ranked_and['url'].extend(ranked_or['url'])
    ranked_and['title'].extend(ranked_or['title'])
    ranked_and['body'].extend(ranked_or['body'])

    end_result = {
        'index': [],
        'title': [],
        'body': [],
        'url': []
    }
    for index, item in enumerate(ranked_and['index']):
        if item not in end_result['index']:
            end_result['index'].append(item)
            end_result['title'].append(ranked_and['title'][index])
            end_result['body'].append(ranked_and['body'][index])
            end_result['url'].append(ranked_and['url'][index])
    return end_result, (time.time() - start_time)


def ranking(indexes, query):
    global read_files
    path_name = "C:\\Users\\Click\\PycharmProjects\\search engine\\combine files"
    resp = {
        'index': [],
        'title': [],
        'body': [],
        'url': [],
    }

    rest = {
        'index': [],
        'title': [],
        'body': [],
        'url': [],
    }

    if search('NOT', query):
        query = query.replace('NOT ', '')
        words = query.split(' ')
        for index in indexes:
            # with open(f'''{path_name}\\{'combine'}-{index}.txt''', 'r',
            #           encoding='utf-8') as f:
            #     read = f.read()
            read = read_files[int(index)].split(' /**********/ ')
            url = read[0]
            title = read[1]
            body = read[2]
            if search(words[0], title):
                resp['index'].insert(0, index)
                resp['url'].insert(0, url)
                resp['title'].insert(0, title)
                resp['body'].insert(0, body)
            else:
                resp['index'].append(index)
                resp['url'].append(url)
                resp['title'].append(title)
                resp['body'].append(body)
        return resp

    else:
        if search('AND', query):
            query = query.replace('AND ', '')
        elif search('OR', query):
            query = query.replace('OR ', '')

        for index in indexes:
            # with open(f'''{path_name}\\{'combine'}-{index}.txt''', 'r',
            #           encoding='utf-8') as f:
            #     read = f.read()
            read = read_files[int(index)].split(' /**********/ ')
            url = read[0]
            title = read[1]
            body = read[2]

            if search(query, title):
                resp['index'].insert(0, index)
                resp['url'].insert(0, url)
                resp['title'].insert(0, title)
                resp['body'].insert(0, body)
            elif search(query, body):
                resp['index'].append(index)
                resp['url'].append(url)
                resp['title'].append(title)
                resp['body'].append(body)
            else:
                resp['index'].append(index)
                rest['url'].append(url)
                rest['title'].append(title)
                rest['body'].append(body)

        resp['index'].extend(rest['index'])
        resp['url'].extend(rest['url'])
        resp['title'].extend(rest['title'])
        resp['body'].extend(rest['body'])
        return resp
