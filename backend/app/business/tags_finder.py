import re


def check_string_is_substring(text, pos, length):
    acceptable_chars = [' ', ',', '\n']
    prev_char = text[pos - 1]
    next_char = text[pos + length]

    is_prev_fine = False
    if pos - 1 > 0:
        is_prev_fine = True
    else:
        is_prev_fine = prev_char in acceptable_chars

    if pos + length >= len(text):
        is_next_fine = True
    else:
        is_next_fine = next_char in acceptable_chars
    return not (is_next_fine and is_prev_fine)


def is_tag_in_text(tag, text) -> bool:
    for currentTag in tag.split('|'):
        currentTag = currentTag.replace('-', ' ')
        pos = 0
        # tag textte birden fazla yerde gecebilir
        # bu yüzden while ile tum eslesmeleri kontrol ediyoruz.
        while pos < len(text):
            pos = text.find(currentTag, pos)
            if pos == -1:
                break
            if (not check_string_is_substring(text, pos, len(currentTag))):
                return True
            pos += len(currentTag)
    return False


def export_tags_from_text(text, allTags):
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
