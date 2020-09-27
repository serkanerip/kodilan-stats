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

def exportTagsFromText(text, allTags):
    exportedTags = []
    text = text.lower()
    text = remove_html_tags(text)

    if not 'reactjs' in text:
        text = text.replace('react', 'reactjs')
    if not 'vue.js' in text:
        text = text.replace('vue', 'vue.js')
        text = text.replace('vuejs', 'vue.js')

    replaceChars = ",({)}"
    for char in replaceChars:
        text = text.replace(char, ' ')
    for tag in allTags:
        tag = tag.replace('-', ' ')
        pos = text.find(tag)
        prevChar = pos-1 < 0 and True or (text[pos-1] is ' ' or text[pos-1] is ',' or text[pos-1] is '\n')
        nextChar = pos+len(tag) >= len(text) and True or text[pos+len(tag)] is ' ' or text[pos+len(tag)] is ',' or text[pos+len(tag)] is '\n'
        if tag == "git":
            print(pos, text[pos-1],prevChar, nextChar)
        if pos != -1 and nextChar and prevChar:
            exportedTags.append(tag)
    return exportedTags

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

