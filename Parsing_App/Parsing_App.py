# -*- coding: cp1251 -*-
import requests
from lxml import html

from selenium.webdriver.common.by import By

import undetected_chromedriver as uc

import time
import re
import os

from tkinter import *
from tkinter import ttk

imdb_title, imdb_year, imdb_rating = [], [], []
kp_title, kp_year, kp_rating = [], [], []
imdb_films, kp_films = [], []

def top50_imdb():
    url = 'https://www.imdb.com/chart/top/'
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
               
    page = requests.get(url, headers=headers)

    tree = html.fromstring(page.content)
    
    for i in range(1, 51):
        title = tree.xpath(f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{i}]/div[2]/div/div/div[1]/a/h3/text()')[0]
        imdb_title.append(re.sub("\d{1,2}\. ", '', title))
        imdb_year.append(tree.xpath(f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{i}]/div[2]/div/div/div[2]/span[1]/text()')[0])
        raw_rating = tree.xpath(f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{i}]/div[2]/div/div/span/div/span/@aria-label')[0]
        imdb_rating.append(re.findall("\d{1}\.\d{1}", raw_rating)[0])

    for i in range(50):
        print(f'{i+1}) {imdb_title[i]} - {imdb_year[i]} - {imdb_rating[i]}')
        imdb_films.append((i+1, imdb_title[i], imdb_year[i], imdb_rating[i]))
    page.close()
    
def top50_kinopoisk():
    base_url = 'https://www.kinopoisk.ru/lists/movies/top250/'

    driver = uc.Chrome()

    driver.get(base_url)
    input("Нажмите Enter, если сайт был успешно открыт...")
    #time.sleep(15)
    movies = driver.find_elements(By.CLASS_NAME, "styles_root__ti07r")

    for movie in movies:
        kp_title.append(movie.find_element(By.CLASS_NAME, "base-movie-main-info_mainInfo__ZL_u3").find_element(By.TAG_NAME, "span").text)
        year = movie.find_element(By.CLASS_NAME, "desktop-list-main-info_secondaryTitleSlot__mc0mI").find_element(By.CLASS_NAME, 
                                  "desktop-list-main-info_secondaryText__M_aus").get_property("innerText")
        kp_year.append(re.findall("\d{4}", year)[0])
        rating = movie.find_element(By.CLASS_NAME, "styles_srRoot__WgbFG").get_property("textContent")
        kp_rating.append(re.findall("\d{1}\.\d{1}", rating)[0])

    for i in range(50):
        print(f'{i+1}) {kp_title[i]} - {kp_year[i]} - {kp_rating[i]}')
        kp_films.append((i+1, kp_title[i], kp_year[i], kp_rating[i]))
        
    driver.quit()
    os.system("taskkill /f /im chrome.exe /T")
    

top50_kinopoisk()
print(kp_films)
top50_imdb()
print(imdb_films)

root = Tk()
root.title("Топ 50 фильмов")
root.geometry("750x600") 

 
label = ttk.Label()
label.grid(row = 0, column = 0, columnspan=2)

label_imdb = ttk.Label(text = "IMDB")
label_imdb.grid(row = 1, column = 0)
label_kp = ttk.Label( text = "Кинопоиск" )
label_kp.grid(row = 1, column = 1)
# определяем столбцы
columns = ("top","title", "year", "rating")
tree = ttk.Treeview(columns=columns, show="headings", height=20)
tree.grid(row = 2, column = 0)
 
# определяем заголовки
tree.heading("top", text="Место", anchor=W)
tree.heading("title", text="Название", anchor=W)
tree.heading("year", text="Год", anchor=W)
tree.heading("rating", text="Рейтинг", anchor=W)
 
tree.column("#1", stretch=NO, width=45)
tree.column("#2", stretch=NO, width=330)
tree.column("#3", stretch=NO, width=50)
tree.column("#4", stretch=NO, width=60)

# определяем столбцы
columns = ("top","title", "year", "rating")
tree_2 = ttk.Treeview(columns=columns, show="headings", height=20)
tree_2.grid(row = 2, column = 1)
 
# определяем заголовки
tree_2.heading("top", text="Место", anchor=W)
tree_2.heading("title", text="Название", anchor=W)
tree_2.heading("year", text="Год", anchor=W)
tree_2.heading("rating", text="Рейтинг", anchor=W)
 
tree_2.column("#1", stretch=NO, width=45)
tree_2.column("#2", stretch=NO, width=330)
tree_2.column("#3", stretch=NO, width=50)
tree_2.column("#4", stretch=NO, width=60)
 
# добавляем данные
for film in imdb_films:
    tree.insert("", END, values=film)

for film in kp_films:
    tree_2.insert("", END, values=film)
 
def item_selected_imdb(event):
    selected_people = ""
    find_status = False
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        film = item["values"]
        for i in range(50):
            if film[1] == kp_title[i]:
                find_status = True
                selected_people = f"IMDB: {film} | Кинопоиск: {kp_films[i]}"
                break
        
    print(f"Find?: {find_status}")
    if find_status == False:
            label["text"]="Совпадений не найдено!"
    else:
        label["text"]=selected_people

def item_selected_kp(event):
    selected_people = ""
    find_status = False
    for selected_item in tree_2.selection():
        item = tree_2.item(selected_item)
        film = item["values"]
        for i in range(50):
            if film[1] == imdb_title[i]:
                find_status = True
                selected_people = f"IMDB: {imdb_films[i]} | Кинопоиск: {film}"
                break
    
    print(f"Find?: {find_status}")
    if find_status == False:
        label["text"]="Совпадений не найдено!"
    else:
        label["text"]=selected_people
 
tree.bind("<<TreeviewSelect>>", item_selected_imdb)
tree_2.bind("<<TreeviewSelect>>", item_selected_kp)
 
root.mainloop()