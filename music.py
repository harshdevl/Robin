
from youtube_search import YoutubeSearch
import json
import webbrowser
from selenium import webdriver
from time import sleep

def search_song(term):
    results = YoutubeSearch(term, max_results=10).to_json()
    results = json.loads(results)
    for i in range(10):
        print('result[{}] : '.format(i),results['videos'][i]['title'])
    number = int(input())
    url = results['videos'][number]['url_suffix']
    return url

def play_songs(url):
    # browser = webdriver.Chrome(executable_path=r'C:/Users/ht501/OneDrive/Desktop/chromedriver.exe')
    browser.get("https://www.youtube.com"+url)
    sleep(3)
    play = browser.find_element_by_class_name('ytp-play-button')
    play.click()
    browser.minimize_window()
    return play

