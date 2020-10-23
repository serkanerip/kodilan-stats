import re


def is_tag_in_text(tag, text) -> bool:
    for currentTag in tag.split('|'):
        currentTag = currentTag.replace('-', ' ')
        pos = 0
        # cumle sonundaki nokta ve unlem isareti
        # tagi bulamamasina sebeb oluyor bu yuzne replace ediliyor.
        text = text.replace('.\n', '\n')
        text = text.replace('!\n', '\n')
        # tag textte birden fazla yerde gecebilir
        # bu yüzden while ile tum eslesmeleri kontrol ediyoruz.
        while pos < len(text):
            pos = text.find(currentTag, pos)
            if pos == -1:
                break
            prevChar = pos-1 < 0 and True or (text[pos-1] is ' ' or text[pos-1] is ',' or text[pos-1] is '\n')
            nextChar = pos+len(currentTag) >= len(text) and True or text[pos+len(currentTag)] is ' ' or text[pos+len(currentTag)] is ',' or text[pos+len(currentTag)] is '\n'
            if nextChar and prevChar:
                return True
            pos += len(currentTag)
    return False


def export_tags_from_text(text, allTags, excepts=[]):
    # taglerin en uzun tagden en kisaya gore gelmesi lazım
    # aksi taktirde duzgun calismaz.

    exportedTags = []
    text = text.lower()
    text = remove_html_tags(text)

    # diyelimki text icinde s35, kelimesi geciyor
    # s3 tagi text icinde gecmis ancak aradigimiz bu degil
    # bunun kontrolu icin text icinde bulunan eslesmenin pozisyonunun
    # bir onceki karakterin ve o cumleden sonraki karakterin
    # bosluk , ve ya \n olmasi lazim ki dogru eslesme yapmasi icin
    # bunun icin (Git) gibi gelimelerde parentezler sanki kelimeye dahilmis
    # gibi gorundugu icin bu karakterler boslukla replace ediliyor.

    notReplacedText = text
    for tag in allTags:
        if tag in excepts:
            continue
        replacedText = notReplacedText
        replaceChars = ",({)}/'’\"`;+-"
        for char in replaceChars:
            # replace karakterlerinden biri tag'de geciyor olabilir.
            # bu yuzden sadece tagde yok ise replace yapiyoruz
            # aksi taktirde ex. c++ gibi tagler bulunamaz.
            if char not in tag:
                replacedText = replacedText.replace(char, ' ')
        if is_tag_in_text(tag, replacedText):
            notReplacedText = notReplacedText.replace(tag, '')
            exportedTags.append(tag.split('|')[0])
    return exportedTags


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
