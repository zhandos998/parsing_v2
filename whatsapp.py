from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# import send_to_server
import connect2db
import os
import json
ID = 1

def get_contacts(page):
    # os.system('cls')  # clear cmd
    soup = BeautifulSoup(page, "html.parser")
    pane_side = soup.find('div', id='pane-side')
    listitem = pane_side.find_all('div', attrs={'role': ['listitem']})
    data_list=[]
    for item in listitem:
        data={
            "href":"",
            "subtitle":"",
            "user_name":"",
            "message_time":"",
            "unread":"",
        }

        # data-testid="cell-frame-container"
        # data-testid="cell-frame-title"
        # data-testid="cell-frame-secondary"
        # data-testid="cell-frame-primary-detail"
        try:
            title = item.find('div', attrs={'data-testid': ['cell-frame-title']})
            title = title.getText()
            if 30<len(title):
                title = title[:30]
                title += "..."
            data["href"] = title
        except:
            print("href error")
        try:
            secondary = item.find('div', attrs={'data-testid': ['cell-frame-secondary']})
            data["subtitle"] = secondary.getText()
            if 30<len(data["subtitle"]):
                data["subtitle"] = data["subtitle"][:30]
                data["subtitle"] += "..."
        except:
            print("subtitle error")
        try:
            title = item.find('div', attrs={'data-testid': ['cell-frame-title']})
            title = title.getText()
            if 30<len(title):
                title = title[:30]
                title += "..."
            data["user_name"] = title
        except:
            print("href error")
        try:
            title = item.find('div', attrs={'data-testid': ['cell-frame-primary-detail']})
            title = title.getText()
            data["message_time"] = title
        except:
            print("message_time error")
        try:
            data["unread"] = None
            if data["unread"]:
                data["unread"] = data["unread"].getText()
        except:
            print("unread error")
        data_list.append(data)
    return data_list

def get_chats(href):
    chatlist_classes = driver.find_elements(By.XPATH, "//div[@data-testid='cell-frame-container']")

    for element in chatlist_classes:
        if element.text.find(href) >= 0:
            element.click()
            try:
                driver.find_element(By.XPATH, "//div[@aria-label='Прокрутить вниз']").click()
                time.sleep(0.5)
            except:
                pass
            page = driver.page_source
            soup = BeautifulSoup(page, "html.parser")
            application = soup.find('div', attrs={'role': ['application']})
            # rows = application.find_all('div', attrs={'role': ['row']})
            messages_list = []
            date = ''
            for row in application.contents:
                # focusable-list-item
                if 'class' in row.attrs and 'focusable-list-item' in row.attrs['class']:
                    date = row.getText()
                    continue
                data = {
                        'who':"",
                        'date':"",
                        'time':"",
                        'content':"",
                    }
                
                if row.find('div',class_ = 'message-in'):
                    data['who']=1
                else:
                    data['who']=0
                copyable_text = row.find('div',class_ = 'copyable-text')
                if copyable_text and 'data-pre-plain-text' in copyable_text.attrs:
                    # data['date'] = copyable_text.attrs['data-pre-plain-text'][1:18]
                    data['date'] = copyable_text.attrs['data-pre-plain-text'][8:18]
                    data['time'] = copyable_text.attrs['data-pre-plain-text'][1:6]

                # data-testid="quoted-message"

                quoted_message = row.find('div', attrs={'data-testid': ['quoted-message']})
                if quoted_message:
                    author = quoted_message.find('span', attrs={'data-testid': ['author']})
                    quoted_mention = quoted_message.find('span', attrs={'class': ['quoted-mention']})
                    # Процитированное сообщение
                    data['content']+="(Процитированное сообщение: "+ author +": "+quoted_mention+") -> "
                selectable_text = row.find('span',class_ = 'selectable-text')
                if selectable_text:
                    selectable_text_span = selectable_text.find('span')
                    for item in selectable_text_span.contents:
                        if type(item)==type(selectable_text_span):
                            if 'alt' in item.attrs:
                                data['content'] += item.attrs['alt']
                            else:
                                data['content'] += item
                        else:
                            data['content'] += item
                else:
                    selectable_text = row.find('div',class_ = 'selectable-text')
                    if selectable_text:
                        selectable_text_img = selectable_text.find('img',class_ = 'selectable-text')
                        if selectable_text_img and 'alt' in selectable_text_img.attrs:
                            data['content'] += selectable_text_img.attrs['alt']
                audio_play = row.find('div', attrs={'data-testid': ['audio-play']})
                if audio_play:
                    data['content'] += "Голосовое сообщение"
                messages_list.append(data)
            break
    return messages_list

# def send_message(text):
#     if (len(text)>=1):
#         # btn_send = driver.find_element(By.CLASS_NAME, "btn-send")
#         btn_send = driver.find_element(By.XPATH, "//div[@data-testid='cell-frame-container']")
#         btn_send.send_keys(text)
#         btn_send.click()
#     pass

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")
while True:

    try:
        # f = open("whatsapp.html", "r")
        # page = f.read()
        page = driver.page_source
        data = get_contacts(page)
        contacts_data = {
            "id" : ID,
            # "func" : "contacts_json",
            "messenger" : "whatsapp",
            "data": json.dumps(data, ensure_ascii=False),
        }
        
        connect2db.send_to_db_contact(contacts_data)
        result = connect2db.get_link_db(ID)
        # data = get_chats("Дарига",page)
        # print(data)
        if result[2]==None:
            data = get_chats(result[1])
            
            chats_data = {
                "id" : ID,
                # "func" : "chat_json",
                # "messenger" : "telegram",
                "data": json.dumps(data, ensure_ascii=False),
            }
            connect2db.send_to_db_chat(chats_data)
    
    except:
        "Not found!"

    time.sleep(1)


driver.close()


Zz87713985075