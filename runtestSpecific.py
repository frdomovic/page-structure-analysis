import allscripts as con
import difflib
from pymongo import MongoClient


def specific(purl, index):
    client = MongoClient('mongodb://fdomovic:@localhost:27017/')
    db = client['websecradar']

    pages_collection = db.crawled_data_pages_v0
    url_collection = db.crawled_data_urls_v0

    firsthash = ""
    secondhash = ""
    for url in url_collection.find({"url":purl}):
            try:
                arr_len = len(url['checks'])
                firsthash = url['checks'][arr_len-1]['hash']
              
                try:
                    secondhash = url['checks'][arr_len-2]['hash']
                   
                    
                    firstpage = ""
                    secondpage = ""
                    
                    for obj in pages_collection.find({"hash":firsthash}):
                        firstpage = obj['page']
                        

                    for obj in pages_collection.find({"hash":secondhash}):
                        secondpage = obj['page']

                    fil1 = con.getParsedPageDB(firstpage)
                    

                    fil2 = con.getParsedPageDB(secondpage)

                    name = purl
                    name = name.replace("https://","")
                    name = name.replace("http://","")
                    if "/" in name:
                        name = name[0:name.index("/")]
                    name2 = name
                    name = str('./rezLimitFile/'+str(index)+'_'+str(firsthash[13:17])+'_'+name+'_1.txt')
                    name3 = str('./rezLimitFile/'+str(index)+'_'+str(secondhash[13:17])+'_'+name2+'_2.txt')
                    name4 = str('./rezLimitFile/'+str(index)+'_'+str(firsthash[13:17])+'_'+name2+'_3.html')


                    difference = difflib.HtmlDiff(wrapcolumn=40).make_file(fil1.split("\n"),fil2.split("\n"),name,name3,True)    
                    diff_report = open(name4, 'w')
                    diff_report.write("")
                    diff_report.write(difference)
                    diff_report.close()
                    

                    f = open (name,'w')
                    f.write(str(fil1))
                   

                    f = open(name3, "w")
                    f.write(str(fil2))
                    f.close()
                

                except:
                    try:
                        print("SPECIFIC ",url['url']," V0 does not have previus versions!")
                        
                    except:
                        print("SPECIFIC, Error getting pages")
                        
            except:
                try:
                    print("SPECIFIC ",url['url']," V1 does not have saved any versions!")
                    
                except:
                    print("SPECIFIC, Error getting pages")
