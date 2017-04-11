from urllib2 import Request, urlopen
import time

null=None
false=False
true=True
headers={
    'Accept': 'application/json'
}

link1='http://api.themoviedb.org/3/genre/878/movies?api_key=65bd6f071e3f5a37f2f0f6dd45f21d43&page='
page=1
count=0
movieID=[]

while count<300:
    link2=str(page)
    link=link1+link2
    request=Request(link,headers=headers)
    response_body=urlopen(request).read()
    movie_List=list(eval(response_body)['results'])
    page=page+1
    for movie in movie_List:
        if count<300:
            movie_title=movie["original_title"]
            movie_id=movie["id"]
            movie_date=movie["release_date"]
            if int(movie_date[0]) > 1 :
                movieID.append(movie_id)
                print(str(movie_id)+", "+movie_title+"\n")
                count=count+1

simPair=[]
link3='http://api.themoviedb.org/3/movie/'
link5='/similar?api_key=65bd6f071e3f5a37f2f0f6dd45f21d43'
for i in movieID:
    link4=str(i)
    link=link3+link4+link5
    request=Request(link,headers=headers)
    response_body=urlopen(request).read()
    simMovie_List=list(eval(response_body)['results'])
    count=0
    for movies in simMovie_List:
        simID=movies["id"]
        if count==5:
            break
        elif (simID, i) in simPair:
            if simID>i:
                pair=(i, simID)
                del simPair[simPair.index((simID, i))]
                simPair.append(pair)
        else:
            pair=(i, simID)
            simPair.append(pair)
        count=count+1
    time.sleep(0.25)
simPairSet=set(simPair)
for pair in simPairSet:
    ID1,ID2=pair
    print (str(ID1)+', '+str(ID2)+'\n')