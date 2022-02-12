from bs4 import BeautifulSoup as bs
from bs4.element import NavigableString

REMOVE_ATTRIBUTES = ['lang','href','language','onmouseover','onmouseout','script','style','font',
                        'dir','face','size','color','style','width','height','hspace',
                        'border','valign','align','background','bgcolor','text','link','vlink',
                        'alink','cellpadding','cellspacing','id','class','clear','action','name','type','title','value','autocomplete'
                        ,'nowrap','alt','src','nonce','content','property','itemprop','itemscope','data-script-url','maxlength','max','min'
                        ,'height','width',
                        'target','http-equiv','placeholder','hidden', 'itemtype','method','for','selected','aria-label',
                        'data-label','rel',',role','data-src','srcset','data-srcset','loading','sizes']


#IZBACIVANJE INNERHTML TEXTA
def remove_text(soup):
    contents = []
    
    for element in soup.contents:
        if not isinstance(element, NavigableString):
            contents.append(remove_text(element))
            
    soup.contents = contents
    return soup

#SAMO HTML TAGOVI
def onlyTagsDB(dbpage):
    soup = bs(dbpage, 'lxml')
    for tag in soup.find_all():
        tag.attrs = {} 
    soup = remove_text(soup)
    return soup.prettify()

#PARSIRANJE CIJELE STRANICE
def getParsedPageDB(dbpage):
  
    soup = bs(dbpage, 'lxml')
    soup = remove_text(soup)
    return(soup.prettify())


#HTML TAGOVI + ATRIBUTI BEZ VRIJEDNOSTI
def removeAttrValuesDB(dbpage):
    soup = bs(dbpage, 'lxml')

    for attr_del in REMOVE_ATTRIBUTES:
        for i in soup.findAll():
            if(attr_del in i.attrs):
                i[attr_del]=''

    soup = remove_text(soup)
    return soup.prettify()


