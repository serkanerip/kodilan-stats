import re

def exportTagsFromTextOld(text, allTags):
    exportedTags = []
    text = text.lower()
    text = remove_html_tags(text)
    replaceChars = ",({)}"
    for char in replaceChars:
        text = text.replace(char, ' ')
    textArr = set(text.split(' '))
    for tag in allTags:
        if tag in textArr:
            exportedTags.append(tag)
    return exportedTags


def is_tag_in_text(tag, text) -> bool:
    tag = tag.replace('-', ' ')
    # react gecen kelimeler reactjs'e cevrildigi icin
    # react-native tagini bulamiyor bu yüzden tagi sanki
    # reactjs native gibiymis gibi gösteriyoruz.
    if tag == 'react native':
        tag = 'reactjs native'
    pos = 0
    # tag textte birden fazla yerde gecebilir bu yüzden while ile tum eslesmeleri kontrol ediyoruz.
    while pos < len(text):
        pos = text.find(tag, pos)
        if pos == -1:
            break
        prevChar = pos-1 < 0 and True or (text[pos-1] is ' ' or text[pos-1] is ',' or text[pos-1] is '\n')
        nextChar = pos+len(tag) >= len(text) and True or text[pos+len(tag)] is ' ' or text[pos+len(tag)] is ',' or text[pos+len(tag)] is '\n'
        if (nextChar and prevChar):
            # apache kafka gibi tagler geldigi zaman tekrar apache icinde bulmasin diye tagi cumleden cikar.
            return True
        pos += len(tag)
    return False

def exportTagsFromText(text, allTags):
    # taglerin en uzun tagden en kisaya gore gelmesi lazım yoksa duzgun calismaz.
    exportedTags = []
    text = text.lower()
    text = remove_html_tags(text)

    # ayni anlama gelip farkli yazilabilen tagleri bulabilmesi icin replaceler
    if not 'ruby on rails' in text:
        text = text.replace('rails', 'ruby on rails')
    if not 'reactjs' in text:
        text = text.replace('react', 'reactjs')
    if not 'vue.js' in text:
        text = text.replace('vue', 'vue.js')
        text = text.replace('vuejs', 'vue.js')
    if 'nodejs' in text:
        text = text.replace('nodejs', 'node.js')
    if not 'css3' in text:
        text = text.replace('css', 'css3')
    if not 'html5' in text:
        text = text.replace('html', 'html5')
    if not 'apache kafka' in text:
        text = text.replace('kafka', 'apache kafka')
    if 'ingilizce' in text:
        text = text.replace('ingilizce', 'english')

    # diyelimki text icinde s35, kelimesi geciyor s3 tagi text icinde gecmis oluyor ancak aradigimiz bu degil
    # bunun kontrolu icin text icinde bulunan eslesmenin pozisyonunun bir onceki karakterin ve o cumleden sonraki karakterin
    # bosluk , ve ya \n olmasi lazim ki dogru eslesme yapmasi icin
    # bunun icin (Git) gibi gelimelerde parentezler sanki kelimeye dahilmis gibi gorundugu icin
    # bu karakterler boslukla replace ediliyor.
    replaceChars = ",({)}/"
    for char in replaceChars:
        text = text.replace(char, ' ')
    
    for tag in allTags:
        if is_tag_in_text(tag, text):
            text = text.replace(tag, '')
            exportedTags.append(tag)
    return exportedTags

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

