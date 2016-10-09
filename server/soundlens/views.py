from django.http import HttpResponse
from django.shortcuts import redirect
import json
import requests
import spotipy
import spotipy.util as util
import tweepy
import base64

# curl -X POST "https://api.clarifai.com/v1/token/" \
#   -d "client_id={client_id}" \
#   -d "client_secret={client_secret}" \
#   -d "grant_type=client_credentials"

# "Authorization: Bearer {access_token}"
#
# curl "https://api.clarifai.com/v1/tag/" \
#   -F "model=general-v1.3" \
#   -F "encoded_data=@/Users/USER/my_image.jpeg" \
#   -H "Authorization: Bearer {access_token}"
#
#   curl "https://api.clarifai.com/v1/tag/?model=general-v1.3&url=https://samples.clarifai.com/metro-north.jpg" \
#    -H "Authorization: Bearer {access_token}"

#d1075499bec940ad9d0d2aa09a6509bd - client_id
#c8ae02f219604c0fa9e074ad1a7d5494 - secret

SPOTIPY_CLIENT_ID = 'd1075499bec940ad9d0d2aa09a6509bd'
SPOTIPY_CLIENT_SECRET = 'c8ae02f219604c0fa9e074ad1a7d5494'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/spot2'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'
MS_COGNITAVE_SUBSCRIPTION = '92d2ca92b1224e83989a7e758e6f4d02'
TWITTER_CONSUMER_KEY = 'vyqW3F9rXy3va4rtvKMwmGfyz'
TWITTER_CONSUMER_SECRET = 'R3JZwKl9Lc66vxKIauTdVCgcC0NHESWtGB3wuaMYWr7PPi3xEp'


sp_oauth = spotipy.oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE );

def spotGetOAuth(request):
    return HttpResponse("HI");

def home(request):
    return HttpResponse("HI");


def getKeys(request):
    print(sp_oauth);
    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.get_full_path();
        code = sp_oauth.parse_response_code(url)
        if code:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...");
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']
        else:
            print('You fucked it')

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        print(results);
        return HttpResponse(results);
    return HttpResponse("<a href='" + sp_oauth.get_authorize_url() + "'>Login to Spotify</a>");

def getTweets(request):
    response_tweets = []
    queries = [
        "boat",
        "water"
    ]
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    api = tweepy.API(auth)

    for query in queries:
        tweets = []
        results = api.search(query, 'en')
        print(str(len(results)) + " results for " + query)
        for result in results:
            response_tweets.append(result.text)
        #print(statuses[0]['text'])
        #query_response = requests.get('https://api.twitter.com/1.1/search/tweets.json?q='+query+"&lang=en")
        #print(query_response.json())
        #for tweet in query_response.json()['statuses']:
        #    tweets.append(tweet['text'])
        #response_tweets.append(tweets)


    headers = {
        "Ocp-Apim-Subscription-Key": MS_COGNITAVE_SUBSCRIPTION,
        "Content-Type": "application/json"
    }
    documents = []
    i = 1
    for document in response_tweets:
        documents.append({
            #"language": "en",
            "id": str(i),
            "text": document
        })
        i += 1
    #print(documents)
    req = requests.post("https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment", json={"documents" : documents}, headers=headers).json()
    scoresum = 0.0
    for response in req['documents']:
        scoresum += response['score']
    score = scoresum / len(req['documents'])
    return HttpResponse(score)

def getEmotions(request):
    tempInfo = {
        'docs' : ["Wow I'm so excited to hear this awesome music", "This fantastic thing is going to be great"] # meh it works for the demo
    }

    headers = {
        "Ocp-Apim-Subscription-Key": MS_COGNITAVE_SUBSCRIPTION,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    documents = []
    i = 1
    input_documents = tempInfo['docs']
    for document in input_documents:
        documents.append({
            "language": "en",
            "id": str(i),
            "text": document
        })
        i += 1
    print(documents)
    req = requests.post("https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment", data={"documents" : documents}, headers=headers)
    return HttpResponse(req)

def submitImg(request):
    imgSrc = request.GET.get('imgSrc', 'null');
    if (imgSrc == 'null'):
        return HttpResponse("The image source you submitted was undefined");
    rq = requests.post("https://api.clarifai.com/v1/token/", data = {'client_id':'dO_TE1MlMpCBeR9SYDL3KVKldKnRfBzlqGU4yGwT',
                                                                    'client_secret':'2DpZgu07HXcMeTWnFRDOLgVd2kVyzNmcWiDNx7Kj',
                                                                    'grant_type':'client_credentials'});
    #print(rq.json());
    accessToken = rq.json()['access_token'];
    #print(accessToken);
    # Post image to Clarifai
    rq = requests.post("https://api.clarifai.com/v1/tag/", data = {'model':'general-v1.3',
                                                                    'url':imgSrc},
                                                           headers = {'Authorization':'Bearer ' + accessToken});
    print(rq.json());
    resp = rq.json();
    #resp = json.loads('{"status_code": "OK", "results": [{"result": {"tag": {"concept_ids": ["ai_HLmqFqBf", "ai_fvlBqXZR", "ai_Xxjc3MhT", "ai_6kTjGfF6", "ai_RRXLczch", "ai_VRmbGVWh", "ai_SHNDcmJ3", "ai_jlb9q33b", "ai_46lGZ4Gm", "ai_tr0MBp64", "ai_l4WckcJN", "ai_2gkfMDsM", "ai_CpFBRWzD", "ai_786Zr311", "ai_6lhccv44", "ai_971KsJkn", "ai_WBQfVV0p", "ai_dSCKh8xv", "ai_TZ3C79C6", "ai_VSVscs9k"], "classes": ["train", "railway", "transportation system", "station", "train", "travel", "tube", "commuter", "railway", "traffic", "blur", "platform", "urban", "no person", "business", "track", "city", "fast", "road", "terminal"], "probs": [0.9989112019538879, 0.9975532293319702, 0.9959157705307007, 0.9925730228424072, 0.9925559759140015, 0.9878921508789062, 0.9816359281539917, 0.9712483286857605, 0.9690325260162354, 0.9687051773071289, 0.9667078256607056, 0.9624242782592773, 0.960752010345459, 0.9586490392684937, 0.9572030305862427, 0.9494642019271851, 0.940894365310669, 0.9399334192276001, 0.9312160611152649, 0.9230834245681763]}}, "local_id": "", "status_code": "OK", "docid_str": "76961bb1ddae0e82f683c2fd17a8794e", "status_msg": "OK", "docid": 17763255747558799694, "url": "https://samples.clarifai.com/metro-north.jpg"}], "status_msg": "All images in request have completed successfully. ", "meta": {"tag": {"model": "general-v1.3", "config": "None", "timestamp": 1475939014.659398}}}')

    if resp['status_code'] != 'OK': #The return value was baaaad!!
        return HttpResponse("There was an issue converting you image:<br>" + resp['status_msg'])

    print(resp['results'][0]);
    if resp['results'][0]['status_code'] != 'OK':
        return HttpResponse("There was an issue converting you image (it is in the results):<br>" + resp['results'][0]['status_msg'])


    output = '<table><tr><th>Class</th><th>Probiblity</th></tr>'
    for i in range(len(resp['results'][0]['result']['tag']['probs'])): #'classes'
        output += '<tr><td>' + resp['results'][0]['result']['tag']['classes'][i] + '</td><td>' + str(resp['results'][0]['result']['tag']['probs'][i]) + '</td></tr>'
    output += '</table>';
    return HttpResponse(output);
