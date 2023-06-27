import os
import time
import youtube_dl
from idm import IDMan
import comtypes.client
from comtypes.gen import IDManLib

def extractor(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info_dict)
    return info_dict, filename

def file_already_exist(script_dir, filename):
    for file in os.listdir(script_dir):
        if os.path.isfile(file):
            name, file_ext = os.path.splitext(file)
            filename2, file_ext = os.path.splitext(filename)
            if filename2 in name:
                return True

    return False

script_dir = os.path.dirname(os.path.abspath(__file__))



downloader = IDMan()
destination_path = r"" # The folder path you want your downloading video to be saved

ydl_opts = {
    'limit_rate' : '128M',
    'proxy': 'socks5://127.0.0.1:10808',
    'verbose': True,
    'outtmpl': '%(title)s-%(id)s.%(ext)s',
    'format':'best',
}
            

# Open the input file
with open('list.txt', 'r') as input_file:

    # Read the list of YouTube URLs from the input file
    youtube_urls = input_file.readlines()

    # Iterate over the list of YouTube URLs
    for i, url in enumerate(youtube_urls, start=1):
        info, filename = extractor(url)
        name, ext = os.path.splitext(filename)
        title = info['title'] 
        width = info['width']
        height = info['height']
        ext = info['ext']
        download_url = info['url']
        # Check if the URL is already in the output file
        if not file_already_exist(script_dir, filename):
            # Process the URL here
            try:
                downloader.download(download_url,path_to_save = destination_path, output=filename, referrer= url, cookie=None, postData=None, user=None, password=None, confirm = False, lflag = None, clip=False)

                while True:
                    if os.path.exists(filename):
                        print(f'{filename} download complete!')
                        break
                    else:
                        print(f'{filename} not found. Waiting 20 seconds...')
                        time.sleep(20)
            


            except KeyboardInterrupt:
                print("Script interrupted by user.")
                break
            except Exception as e:
                print("************** Failed **************")
                print(e)
        else:
            print("************** SKIPPED . ALREADY EXIST **************")

# Close the input file
input_file.close()

