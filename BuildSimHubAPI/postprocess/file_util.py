
def save_file(content, directory):
    text_file = open(directory, 'w')
    text_file.write(content)
    text_file.close()
