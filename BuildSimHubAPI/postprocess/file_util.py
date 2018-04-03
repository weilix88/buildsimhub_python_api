
def save_file(content, dir):
    text_file = open(dir, 'w')
    text_file.write(content)
    text_file.close()
