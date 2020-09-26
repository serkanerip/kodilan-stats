def exportTagsFromText(text, allTags):
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

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

