from bs4 import BeautifulSoup
import os

def parse(page):
    os.system('cls')
    soup = BeautifulSoup(page, "html.parser")
    chat_list = soup.find('ul', class_='chatlist')
    chat_list = chat_list.findAll('div', class_='user-title')
    for title in chat_list:
        print(title.getText())
    # print(chat_list)

    
def get_active_message(href):
    os.system('cls')
    soup = BeautifulSoup(page, "html.parser")
    chat_list = soup.find('ul', class_='chatlist')
    chat_list = chat_list.findAll('div', class_='user-title')
    for title in chat_list:
        print(title.getText())