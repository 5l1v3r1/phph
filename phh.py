import requests, re, json
import urllib.parse as urlparse


def get(url):
    q_240p = None
    q_140p = None
    if 'http' in url:
        vkey = urlparse.parse_qs((urlparse.urlparse(url).query))['viewkey'][0]
    else:
        vkey = url
        url = 'https://pornhub.com/view_video.php?viewkey='+vkey
    apiurl = 'https://api.pornhub.com/api_android_v3/getVideo'
    params = {'appKey':'72d2512a43364263e9d94f0f73',
              'userId':'72956112',
              'userKey':'5d9556eee5dbb002c4d5aac4c5cfb327b54261f658eda5f581b7555edbe72c31',
              'vkey': vkey,
              'uuid':'1'}
    info = requests.get(apiurl, params=params).json()
    with open('cookies.json', 'r') as f:
            cookies = json.loads(f.read().replace("'", '"'))
    if 'pornhubpremium' not in url:
            url = url.replace('pornhub', 'pornhubpremium')
    r = requests.get(url, headers = {'User-Agent':'Mozilla/5.0'}, cookies = cookies)
    if '240P' in r.content.decode("utf-8"):
            q_240p = re.search('"quality":"240","videoUrl":"(.*?)"},', r.content.decode("utf-8")).group(1).replace('\\', '')
    if '140P' in r.content.decode("utf-8"):
            q_140p = re.findall('<a class="downloadBtn greyButton" href="(.*?)" ', r.content.decode("utf-8"))[-1]
    result = {}
    result['title'] = info['video']['title']
    result['duration'] = info['video']['duration']
    videos = json.loads(re.search(r"{'\d+\w':\s'https:\/\/.+\/videos.+.mp4.+',\s'2160p_available'", str(info['video']['encodings'])).group().replace(", '2160p_available'", '}').replace("'", '"'))
    if q_240p != None:
        videos['240p'] = q_240p
        result['videos'] = videos
    if q_140p != None:
        videos['140p'] = q_140p
        result['videos'] = videos
    else: result['videos'] = videos
    result['qualitys'] = list(videos)
    return result
    
