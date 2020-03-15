from requests import get
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import sleep
from numpy import random
import pandas as pd


def get_books(url):
    """
    This function is to collect the html information with specific
    label from the target url

    Args:
        url (str): url of the target web page

    Returns:
        books (bs4.element): results of the html label search of the books

    """

    # Generate a fake header
    user_agent = UserAgent()

    # Request and collect html information of the books
    response = get(url, headers={'user-agent': user_agent.random})
    html_soup = BeautifulSoup(response.text, 'html.parser')
    books = html_soup.find_all('div', class_='type02_bd-a')

    return books


# Collect the category and original price info for the book
def get_info(book_input):
    """
    This function collects the category and original price information
    of the book

    Args:
        book_input (bs4.element): the html information of the book

    Returns:
        sub_cats (list): the category information of the book
        price_original (int): the original price of the book

    """

    # Get the url of the book
    book_url = book_input.h4.a.attrs['href']

    # Generate a fake header
    user_agent = UserAgent()

    # Request and collect html information of the book
    response_info = get(book_url, headers={'user-agent': user_agent.random})
    html_soup = BeautifulSoup(response_info.text, 'html.parser')

    # Find the category and original price information
    category = html_soup.find_all('ul', class_='container_24 type04_breadcrumb')
    sub_cats = [sub_cat.text for sub_cat in category[0].find_all('span')]
    price = html_soup.find_all('ul', class_='price')

    # if there is no original price information
    if len(price) == 0:
        return sub_cats, 'NA'

    # if there is price information
    elif len(price) != 0:
        price_original = int(price[0].em.text)
        return sub_cats, price_original


def get_price(book_input):
    """
    This function collects the special price information of the book

    Args:
        book_input (bs4.element): the html information of the book

    Returns:
        price (int): the special price of the book

    """

    # Find the special price information
    price_label = book_input.find_all('li', class_='price_a')[0].find_all('b')

    # If there is no discount
    if len(price_label) == 1:
        price = int(price_label[0].text)
        return price

    # If there is a discount
    elif len(price_label) == 2:
        price = int(price_label[1].text)
        return price


def collect(books):
    """
    This function collects all the required information of the books

    Args:
        books (bs4.element): the html information of the books

    Returns:
        collection (dict): a collection of the required information

    """

    names = []
    authors = []
    book_urls = []
    categories = []
    prices_original = []
    prices_special = []

    # Collect book names, authors, urls and special price
    for i, book in enumerate(books):
        print('Number {}'.format(i+1))
        print(book.h4.a.text)
        print('')
        names.append(book.h4.a.text)
        authors.append(book.ul.li.text.split('：')[1])
        book_urls.append(book.h4.a.attrs['href'])
        prices_special.append(get_price(book))

    # Collect category and special price
    for i, book in enumerate(books):
        info = get_info(book)
        print('Number {}'.format(i+1))
        print(info)
        print('')
        categories.append(info[0])
        prices_original.append(info[1])

        # Set up a 60" - 90" time delay for each round of collection
        sleep(random.randint(60, 90))

    # Pack all the collected information
    collection = {
        'names': names,
        'authors': authors,
        'book_urls': book_urls,
        'categories': categories,
        'prices_original': prices_original,
        'prices_special': prices_special
        }

    print('-'*10 + 'Data collection complete' + '-'*10)
    print('')

    return collection


def output_file(collection):
    """
    This function outputs the collected information to json file
    in the work folder

    Args:
        collection (dict): a collection of the required information

    Returns:
        None

    """

    # Create a dataframe from the collected information
    df = pd.DataFrame(columns=['Name', 'Author', 'Category_1',
                               'Category_2', 'Category_3', 'Category_4',
                               'Price_original', 'Price_special'])

    df['Name'] = collection['names']
    df['Author'] = collection['authors']

    df['Category_1'] = [row[1] for row in collection['categories']]
    df['Category_2'] = [row[2] for row in collection['categories']]
    df['Category_3'] = [row[3] for row in collection['categories']]
    df['Category_4'] = [row[4] for row in collection['categories']]

    df['Price_original'] = collection['prices_original']
    df['Price_special'] = collection['prices_special']

    # Output the dataframe to json files
    with open('book.json', 'w', encoding='utf-8') as file:
        df.to_json(file, force_ascii=False)

    print('-'*10 + 'File output complete' + '-'*10)


# Collect the html information of the books in the target web page
books = get_books('https://www.books.com.tw/web/sys_tdrntb/books/')

# Collect the required information of hte books
collection = collect(books)

# Output the json file
output_file(collection)
