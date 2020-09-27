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
    for currentTag in tag.split('|'):
        currentTag = currentTag.replace('-', ' ')
        pos = 0
        # tag textte birden fazla yerde gecebilir bu yüzden while ile tum eslesmeleri kontrol ediyoruz.
        while pos < len(text):
            pos = text.find(currentTag, pos)
            if pos == -1:
                break
            prevChar = pos-1 < 0 and True or (text[pos-1] is ' ' or text[pos-1] is ',' or text[pos-1] is '\n')
            nextChar = pos+len(currentTag) >= len(text) and True or text[pos+len(currentTag)] is ' ' or text[pos+len(currentTag)] is ',' or text[pos+len(currentTag)] is '\n'
            if (nextChar and prevChar):
                # apache kafka gibi tagler geldigi zaman tekrar apache icinde bulmasin diye tagi cumleden cikar.
                return True
            pos += len(currentTag)
    return False

def exportTagsFromText(text, allTags):
    # taglerin en uzun tagden en kisaya gore gelmesi lazım yoksa duzgun calismaz.
    exportedTags = []
    text = text.lower()
    text = remove_html_tags(text)

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
            exportedTags.append(tag.split('|')[0])
    return exportedTags

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

