def get_tags_from_csv(csvFilePath):
    with open(csvFilePath) as reader:
        content = reader.read()
        content = content.replace('"', "")
        content = content.replace("><", ",")
        content = content.replace("<", "")
        content = content.replace(">", "")
        content = content.replace("\n", ",")
        tags = content.split(",")
        excludes = get_excluded_words('excluded_words.txt')
        tagsSet = set(tags)
        tagsSet = [x for x in tagsSet if len(x) > 2]
        tagsSet = [x for x in tagsSet if not 'android-' in x]
        tagsSet = [x for x in tagsSet if not x in excludes]
        return [x for x in tagsSet if not x.replace('.', '').replace(',', '').isnumeric()]


def get_excluded_words(filename):
    with open(filename, 'r') as reader:
        content = reader.read()
        return content.split('\n')
