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


# Define the wait time in seconds
wait_time = 1200  # 10 minutes


downloader = IDMan()
destination_path = r"" # The folder path you want your downloading video to be saved

ydl_opts = {
    'limit_rate' : '128M',
    'proxy': 'socks5://127.0.0.1:10808',
    'verbose': False,
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

                start_time = time.time()
                downloaded = False
                total_seconds = 0 

                while not downloaded and (time.time() - start_time) < wait_time:
                    minutes_old = total_seconds // 60  # Integer division to get the number of minutes
                    minutes = (total_seconds+1) // 60  # Integer division to get the number of minutes
                    seconds_old = total_seconds % 60  # Modulo operator to get the number of remaining seconds
                    seconds = (total_seconds+1) % 60  # Modulo operator to get the number of remaining seconds
                    output_string = f'{filename} not found. {minutes} Minutes and {seconds} Seconds...'
                    if os.path.exists(filename):
                        # prevent \r to override last output
                        print(output_string)
                        downloaded = True
                    else:
                        print(output_string, end="\r")

                    time.sleep(1)
                    total_seconds = total_seconds + 1

            
                if not downloaded:
                    print(f'Timeout exceeded for {filename}, moving on to the next URL...')
                    continue

                # Video downloaded successfully
                print(f'{filename} downloaded successfully!')

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
