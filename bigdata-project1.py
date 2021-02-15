from bs4 import BeautifulSoup
from random import randint
import requests
import time
## attributes / config file for Spider class -- TODO
parsed_file_path = 'parsed.txt'

binance_htmls_path = 'binance_htmls/'
uniswap_htmls_path = 'uniswap_htmls/'
coinbase_htmls_path = 'coinbase_htmls/'

binance_cols = 6
uniswap_cols = 10

binance_header = 5
uniswap_header = 10

binance_remove_first = 0
uniswap_remove_first = 10

base = 'http://www.coinranking.com/exchange/-zdvbieRdZ+binance/markets'
pages = [base + f'?page={i}' for i in range(2, 19)]
pages.insert(0, base)

binance_files = [str(i)+'.txt' for i in range(len(pages))]
uniswap_files = ['0.txt']
coinbase_files = ['0.txt']

def initialize(pages=None, htmls_path=None):
    files = []
    for i, page in enumerate(pages):
        file = str(i) + '.txt' 
        response = None
        try:
            response = requests.get(page)
        except Exception:
            print('Couldnt fetch page. Failed to generate file.')
            print(f'{page} -> {file}')
            continue
        file_path = htmls_path + file
        files.append(file)
        bs = BeautifulSoup(response.text, 'lxml')
        open(file_path, 'w', encoding='utf-8')
        with open(file_path, 'a', encoding='utf-8') as out:
            out.write(bs.prettify())
        if len(pages) > 1:
            time.sleep(1)
            time.sleep(randint(1, 10)/10) 
    return files

def parse(files=None, htmls_path=None, identifier='NoneProvided'):
    header = '\n' + identifier + '\n'
    clean_more = dc.get(identifier)
    for file in files:
        bs = None
        with open(htmls_path + file, 'r', encoding='utf-8') as doc:
            bs = BeautifulSoup(doc, 'lxml')
        table = bs.find_all('table')
        with open(parsed_file_path, 'a', encoding='utf-8') as out:
            out.write(header)
            for item in table:
                dirty = item.getText(separator='//', strip=True)
                clean = clean_basic(dirty=dirty)
                clean = clean_more(clean)
                out.write(clean)

def clean_basic(dirty):
    # for production, filter regex on the whole page
    dirty = dirty.replace("[,", '')
    dirty = dirty.replace(",]", '')
    dirty = dirty.replace("[", '')
    dirty = dirty.replace("]", '')
    dirty = dirty.replace('  \n', '')
    dirty = dirty.replace('\n', '')
    dirty = dirty.replace('  ', '')
    clean = dirty.replace(',', '')
    return clean

def clean_cr(line):
    ## identifier upper
    line = line.replace('//Binance//', '//')
    line = 'Rank//' + line
    return line

def clean_cmc(line):
    line = line.replace('//%//', '%//')
    line = line.replace('//***//', '//')
    return line

def split_data(delimiter='//', remove_first=0, line=None):
    arr = line.split(delimiter)
    if (remove_first != 0) and (remove_first < len(arr)):
        del arr[:remove_first]
    return arr

def format_data(arr=None, cols=0, identifier=None, header=None, headarr=None):
    csv_file = identifier + '.csv'
    with open(csv_file, 'a', encoding='utf-8') as out:
        if headarr:
            h = ','.join(headarr)
            h += '\n'
            out.write(h)
        ## remove option, but easier to ignore redundant info columns for now
        for i in range(0,len(arr),cols):
            start = i
            end = i+header
            row = arr[start:end]
            if '\n' in row[-1]:
                continue
            row = ','.join(row) + '\n'
            out.write(row)

def transform(identifiers, file=parsed_file_path):
    configs = dt
    header = None
    for i in identifiers:
        path = i + '.csv'
        open(path, 'w', encoding='utf-8')
    line = None
    with open(parsed_file_path, 'r', encoding='utf-8') as doc:
        lines = doc.readlines()
        line = iter(lines)
        next(line) ## empty line bc wrote to empty
    while True:
        try:
            identifier = next(line).replace('\n', '')
            data = next(line)
            config = configs.get(identifier)
            arr = split_data(remove_first=config.get('remove_first'), line=data)
            header = config.get('header')
            headarr = arr[:header]
            del arr[:header]
            if not config.get('wrote_header'):
                format_data(arr=arr, cols=config.get('cols'), identifier=identifier, header=header, headarr=headarr)
                config.update({'wrote_header': True})
            else: 
                format_data(arr=arr, cols=config.get('cols'), identifier=identifier, header=header)
        except StopIteration:
            break
        except Exception as e:
            print(e)
            break

dc = {
    'uniswap': clean_cmc,
    'binance': clean_cr,
}

dt = {
    'binance': {
        'cols': binance_cols,
        'remove_first': binance_remove_first,
        'header': binance_header,
        'wrote_header': False,
    }, 
    'uniswap': {
        'cols': uniswap_cols,
        'remove_first': uniswap_remove_first,
        'header': uniswap_header,
        'wrote_header': False,
    }
}

if __name__ == '__main__':
    # uniswap_files = initialize(pages=['http://coinmarketcap.com/exchanges/uniswap-v2/'], htmls_path=uniswap_htmls_path)
    # binance_files = initialize(pages=pages, htmls_path=binance_htmls_path)
    open(parsed_file_path, 'w', encoding='utf-8')
    parse(files=binance_files, htmls_path=binance_htmls_path, identifier='binance')
    parse(files=uniswap_files, htmls_path=uniswap_htmls_path, identifier='uniswap')
    transform(['binance', 'uniswap'], file=parsed_file_path)
