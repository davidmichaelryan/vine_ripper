import json
import urllib
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

VINE_URL = "https://vine.co/api/timelines/users/<INSERT_USER_ID>/likes?size=20"

def get_vine_likes(userID):
    print "downloading vines you've liked..."
    
    likes = []
    nextPage = ""
    
    url = str.replace(VINE_URL, "<INSERT_USER_ID>", userID)
    while nextPage != None:
        vineJSON = urllib.urlopen(url)
        vineData = json.load(vineJSON)['data']
        if len(vineData['records']) > 0: 
            likes = likes + vineData['records']
        nextAnchor = vineData['anchor']
        nextPage = vineData['nextPage']
        url = str.replace(VINE_URL, "<INSERT_USER_ID>", userID) + "&page="+str(nextPage)+"&anchor="+str(nextAnchor)
    
    print 'done fetching likes. processing...'

    likeData = []
    for like in likes:
        newObj = {}
        newObj['postId'] = like['postId']
        newObj['username'] = like['username']
        newObj['avatarUrl'] = like['avatarUrl']
        newObj['description'] = like['description']
        newObj['videoUrl'] = like['videoUrl']
        newObj['thumbnailUrl'] = like['thumbnailUrl']

        likeData.append(newObj)

    return likeData

def rip_vines(likeData):
    print 'downloading vines...'
    folderLocation = os.getcwd()
    for like in likeData:
        postId = str(like['postId'])
        username = str(like['username'])
        avatarUrl = str(like['avatarUrl'])
        videoUrl = str(like['videoUrl'])
        thumbnailUrl = str(like['thumbnailUrl'])

        if not os.path.isfile(folderLocation + '/vine_data/avatars/'+ username + '.jpg'):
            urllib.urlretrieve(avatarUrl, folderLocation + '/vine_data/avatars/' + username + '.jpg')
        if not os.path.isfile(folderLocation + '/vine_data/videos/' + postId + '.mp4'):
            urllib.urlretrieve(videoUrl, folderLocation + '/vine_data/videos/' + postId + '.mp4')
        if not os.path.isfile(folderLocation + '/vine_data/video_thumbnails/' + postId + '.jpg'):
            urllib.urlretrieve(thumbnailUrl, folderLocation + '/vine_data/video_thumbnails/' + postId + '.jpg')

def save_to_json(likeData):
    likeJSON = json.dumps(likeData, indent=4, sort_keys=True)
    with open("vine_data/metadata.json", "w") as textFile:
        textFile.write(likeJSON)

def setup_folders():
    for path in ['vine_data/', 'vine_data/avatars', 'vine_data/video_thumbnails', 'vine_data/videos']:
        try: 
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise

def download_like_metadata(userID):
    likeData = get_vine_likes(userID)
    setup_folders()
    save_to_json(likeData)
    print 'vine metadata downloaded'
    return likeData

def main():
    print "This needs a userID to work..."
    print "Go to the profile page for any viner (including yourself) and get the number in the url"

    userID = str(input('enter your userID:  '))
    likeData = download_like_metadata(userID)
    rip_vines(likeData)
    print 'done'

main()
