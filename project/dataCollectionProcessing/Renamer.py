import glob, os

def rename(dir, pattern):
    for filename in glob.iglob(os.path.join(dir, pattern)):
        new_fileName = filename.replace('satellitle.jpeg','_satellitle.jpeg')
        os.rename(filename, new_filename)


rename(r'/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/Satellite-View', r'*.jpeg')