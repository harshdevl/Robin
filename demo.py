import pafy
import os




def download_songs(url,dirs='songs_by_jarvis',parent_dir='D:/python_project/project_jarvis'):
    path = os.path.join(parent_dir, dirs) 
    try: 
        os.makedirs(path, exist_ok = True) 
        print("Directory '%s' created successfully" % dirs) 
    except OSError as error: 
        print("Directory '%s' can not be created" % dirs) 
    url = 'https://www.youtube.com'+url    
    song = pafy.new(url)
    song = song.getbestaudio()
    song.download('songs_by_jarvis/')


def download_video(url,dirs='video_by_jarvis',parent_dir='D:/python_project/project_jarvis'):
    path = os.path.join(parent_dir, dirs) 
    try: 
        os.makedirs(path, exist_ok = True) 
        print("Directory '%s' created successfully" % dirs) 
    except OSError as error: 
        print("Directory '%s' can not be created" % dirs) 
    url = 'https://www.youtube.com'+url
    video = pafy.new(url)
    video = video.getbest()
    video.download('video_by_jarvis/')

def download_playlist(url,dirs='playlsit_by_jarvis',parent_dir='D:/python_project/project_jarvis'):
    path = os.path.join(parent_dir, dirs) 
    try: 
        os.makedirs(path, exist_ok = True) 
        print("Directory '%s' created successfully" % dirs) 
    except OSError as error: 
        print("Directory '%s' can not be created" % dirs)
    url = 'https://www.youtube.com'+url
    playlist = pafy.get_playlist(url)
    playlist = playlist['items']
    for i in playlist:
        i_pafy = i['pafy']
        y_url = i_pafy.getbest()
        y_url.download('playlsit_by_jarvis')
