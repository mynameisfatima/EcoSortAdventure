def classify_trash(trash_name):
    recyclable = ['paper', 'plasticbottle', 'can']
    return 1 if trash_name.lower() in recyclable else 0
