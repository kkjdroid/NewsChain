def get_lines(no_of_pagedowns = 20):
    import time
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from pyvirtualdisplay import Display

    display = Display(visible=0, size=(1920,1080))
    display.start()
    browser = webdriver.Chrome()
    browser.get('http://www.buzzfeed.com')
    time.sleep(1)

    elem = browser.find_element_by_tag_name("body")

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns-=1

    post_elems = browser.find_elements_by_tag_name('h1') + browser.find_elements_by_tag_name('h2')
    lines = [_.text.strip() for _ in post_elems if len(_.text) > 15]
    browser.quit()
    display.stop()
    return lines

def remove_emoji(line):
    import re
    emoji = re.compile('[\U00010000-\U0010ffff]')
    "credit to Martijn Pieters at https://stackoverflow.com/a/12636588"
    return emoji.sub('', line).strip()

def sample_to_file(sample, f = 'sample.txt'):
    workfile = open(f, 'w')
    for l in sample:
        workfile.write(f'{l}\n')

def sample_from_file(f = 'sample.txt'):
    import os
    print(os.getcwd())
    workfile = open(f)
    sample = workfile.readlines()
    return sample
    
"""def find_object(line):
    from spacy.en import English
    nlp = English()
    doc = nlp(line)

    sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]

    return sub_toks or list(doc.noun_chunks)[0]"""
