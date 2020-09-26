excludes = ['and', 'remote', 'building','create','all','services','technologis', 'as', 'az', 'web', 'to', 'for', 'of', 'with', 'the', 'in', 'experience', 'is', 'team', 'or', 'on', 'new', 'knowledge', 'will', 'skills', 'work', 'at', 'from', 'one', 'core', 'using', 'data']

with open('excluded_words.txt', 'w') as writer:
    writer.write("\n".join(excludes))