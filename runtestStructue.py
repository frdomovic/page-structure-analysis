import allscripts as con
import difflib
from pymongo import MongoClient
from datetime import datetime
import runtestSpecific as rts
from bs4 import BeautifulSoup as bs
#del pass 
client = MongoClient('mongodb://fdomovic@localhost:27017/')
db = client['websecradar']

pages_collection = db.crawled_data_pages_v0
url_collection = db.crawled_data_urls_v0

firsthash = ""
secondhash = ""
index = 1

for url in url_collection.find({}).limit(5000):
        try:
            arr_len =  len(url['checks'])
            firsthash = url['checks'][arr_len-1]['hash']
            try:
                
                secondhash = url['checks'][arr_len-2]['hash']
                if(firsthash != secondhash):
                    name = (url['url'])
                    datum1 = str(datetime.fromtimestamp( url['checks'][arr_len-1]['timestamp'])).split(" ")[0]
                    datum2 = str(datetime.fromtimestamp( url['checks'][arr_len-2]['timestamp'])).split(" ")[0]
                    nameref =  datum1+url['url']
                    nameref2 = datum2+url['url']
                    name = name.replace("https://","")
                    name = name.replace("http://","")
                    if "/" in name:
                        name = name[0:name.index("/")]
                    name = str('./structureChange/'+str(index)+'_'+name+'.html')
        

                    firstpage = ""
                    secondpage = ""

                    for obj in pages_collection.find({"hash":str(firsthash)}).limit(1):
                        firstpage = obj['page']

                    for obj in pages_collection.find({"hash":str(secondhash)}).limit(1):
                        secondpage = obj['page']

                    fil1 = con.onlyTagsDB(firstpage)
                    fil2 = con.onlyTagsDB(secondpage)
                   
                    if(fil1 == fil2):
                        print(index,". page is OK | hash1 != hash2 : ", url['url'], "|| HASH: ",url['checks'][arr_len-1]['hash'])
                    else:
                        diffCharStr = "".join(difflib.Differ().compare(fil2,fil1)).replace(" ","")
                        chx = diffCharStr.split('\n')
                        DCList = list(diffCharStr)
                        refrecorDCL = []

                        if(len(chx) > 8):
                            for i in range(0,len(DCList)):
                                if(DCList[i-1] != '-' and DCList[i] != '-'):
                                    refrecorDCL.append(DCList[i])

                            refrecorDCL = "".join(refrecorDCL).replace("+","").split('\n')
                        

                            if(len(refrecorDCL) > 10):
                                print(index,". page is NOT OK changes num +10: ", url['url'], "|| HASH: ",url['checks'][arr_len-1]['hash'])
                                difference = difflib.HtmlDiff(wrapcolumn=40).make_file(fil2.split("\n"),fil1.split("\n"),nameref2,nameref,True)
                                #rts.specific(str(url['url']),index)
                                diff_report = open(name, 'w')
                                diff_report.write("")
                                diff_report.write(difference)
                                diff_report.close()

                            else:
                                print(index,". page is NOT OK (NO CHECK num -10): ", url['url'], "|| HASH: ",url['checks'][arr_len-1]['hash'])    
                        else:
                            print(index,". page is NOT OK (NO CHECK num -10): ", url['url'], "|| HASH: ",url['checks'][arr_len-1]['hash'])    
                else:
                    print(index,". page OK: ", url['url'], "|| HASH: ",url['checks'][arr_len-1]['hash'])
                index += 1

            except:
                try:
                    print(index,". The ",url['url'],"V0 does not have previus versions!")
                    index += 1
                except:
                    print("Error getting pages")
                    index += 1

        except:
            try:
                print(index,". The ",url['url'],"V1 does not have saved any versions!")
                index += 1
            except:
                print("Error getting pages")
                index += 1


