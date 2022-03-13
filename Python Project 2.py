# Isaac Huang, SID: 23019722
def main (WARC_fname, positive_words_fname, negative_words_fname):
    # Catch wrong files or paths error
    try:
        # Extrac pure texts, sentences, and url links from WARC file
        words, sentences, links = txt(extracts(WARC_fname))
        gen_pos = list(gen_au(words, positive_words_fname, negative_words_fname))
        gov_pos = list(gov_au(sentences, positive_words_fname, negative_words_fname))
        pat = list(patriotic(words))
        top_links= link_au(links)
    # Function gracefully terminates and return 4 empty lists
    except FileNotFoundError:
        return [],[],[],[]
    return gen_pos, gov_pos, pat, top_links

def extracts(WARC_fname):
    # Open WARC file in binary mode then decode
    warc_file = open(WARC_fname, 'rb')
    file = warc_file.read().decode('ascii', 'ignore')
    warc_file.close()
    data = []
    # Use 'WARC/1.0' as dividers, then split the chunks into 3 blocks of data
    for chunk in file.split('WARC/1.0'):
        data.append(chunk.split('\r\n\r\n', 2))
    return data

# Extract words, sentences and links from data, then stored in dictionaries
def txt(data):
    words = dict()
    sentences = dict()
    links = dict()
    urlkey = None
    value = None
    sentence = None
    link = None
    for i in range(len(data)):
        if "WARC-Type: response" in data[i][0] and "Content-Type: text/html" in data[i][1]:
            # Use 2 splits to extract target url
            urlkey = data[i][0].split("WARC-Target-URI: ", 1)[1].split("WARC-Payload-Digest", 1)[0].rstrip("\r\n")
            # Remove JavaScripts from data
            data[i][2] = javacleaner(data[i][2])
            link = ahref(data[i][2])
            # Restore all url links in a dictionary called links
            links[urlkey] = link
            # Remove all html tags
            data[i][2] = html_cleaner(data[i][2])
            sentence = keep_dot(data[i][2])
            value = punc_cleaner(data[i][2])
            # Restore all words in a dictionary called words
            words[urlkey] = value
            # Restore all sentences in a dictionary called sentences
            sentences[urlkey] = sentence          
    return words, sentences, links

# Strip all "<a href tags" to get all web domains
def ahref(mystr):
    link = []
    x = "href="
    for a_tag in mystr.split('<a ')[2:]:
        if x in a_tag and "http" in a_tag and '.au' in a_tag and '>' in a_tag:
            # Use 2 splits to get "href=......>
            a_tag = a_tag.split(x,1)[1].split('>',1)[0]
            # We only want 'http:' and 'https:' urls
            if 'http://' in a_tag or 'https://' in a_tag:
                start = a_tag.find('://')+3
                end = a_tag.find('.au', start)
                # Slice strings to get url, then append them in a list
                link.append(a_tag[start:end+3])
    # Return a string with a space key in between
    return " ".join(link)

def javacleaner(mystr):
    # Remove all \n \t \n, and only leave a space key
    mystr = mystr.replace("\n", " ")
    mystr = mystr.replace("\t", " ")
    mystr = mystr.replace("\r", " ")
    # Convert all characters to lowercases
    mystr = mystr.lower()
    x = "<script"
    y = "</script"
    # Use while loop and slice all JavaScripts out
    while x in mystr:
        mystr = mystr[:mystr.find(x)] + mystr[mystr.find(">",mystr.find(y, mystr.find(x)))+1:]
    return mystr

# Remove all html tags
def html_cleaner(mystr):
    while "<" in mystr:
        # Some greater than or less than signs are not paired up
        if mystr.find(">", mystr.find("<")) == -1:
            break
        # Find all paired html tags and slice them out
        mystr = mystr[:mystr.find("<")] + mystr[mystr.find(">",mystr.find("<"))+1:]
    return mystr

# Remove all punctuation
def punc_cleaner(mystr):
    # List all ANSI punctuation in ASCII code
    ASCII = list(range(128))
    chlist = ASCII[33:48]+ASCII[58:65]+ASCII[91:97]+ASCII[123:127]
    # Remove all ANSI punctuation
    for c in chlist:
        mystr = mystr.replace(chr(c), "")
    return mystr

def keep_dot(mystr):
    # Replace ! and ? with a dot
    mystr = mystr.replace('!', '.').replace('?', '.')
    # Remove all other punctuation we don't want
    ASCII = list(range(128))
    chlist = ASCII[33:46]+ASCII[47:49]+ASCII[58:65]+ASCII[91:97]+ASCII[123:127]
    for c in chlist:
        mystr = mystr.replace(chr(c), "")
    return mystr

# Check if the url is an au domain
def domain_au(my_url):
    domain = False
    # Use 2 splits to get url
    token = my_url.split('://')[1].split('/')[0]
    # Check if they are Australian websites
    token = token.replace(':','.').split('.')[-2:]
    if "au" in token:
        domain = True
    return domain

# Count general postive and negative words in Australian websites
def gen_au(dictionary, positive_words_fname, negative_words_fname):
    p_file = open(positive_words_fname, 'r')
    pos = p_file.read().split()
    p_file.close()
    p_count = 0
    n_file = open(negative_words_fname, 'r')
    neg = n_file.read().split()
    n_file.close()
    n_count = 0
    count = 0
    # Check urls we stored as keys in dictionary earlier
    for url in dictionary.keys():
        if domain_au(url):
            count += 1
            # Split values to count positive and negative words
            for word in dictionary.get(url).split():
                if word in pos:
                    p_count += 1
                if word in neg:
                    n_count += 1
    # Preventing ZeroDivisionError
    try:
        a = round(p_count/n_count, 4)
    except ZeroDivisionError:
        a = None
    try:
        b = round(p_count/count, 4)
    except ZeroDivisionError:
        b = None
    try:
        c = round(n_count/count, 4)
    except ZeroDivisionError:
        c = None
    return p_count, n_count, a, b, c

# Count positive and negative sentences towards Australian government
def gov_au(dictionary, positive_words_fname, negative_words_fname):
    p_file = open(positive_words_fname, 'r')
    pos = p_file.read().split()
    p_file.close()
    p_count = 0
    ps_count = 0
    n_file = open(negative_words_fname, 'r')
    neg = n_file.read().split()
    n_file.close()
    n_count = 0
    ns_count = 0
    count = 0
    # Check urls we stored as keys in dictionary earlier
    for url in dictionary.keys():
        if domain_au(url):
            count += 1
            for se in dictionary.get(url).split('.'):
                # Check if 'government' is in the sentence
                if "government" in se.split():
                    for i in se.split():
                        if i in pos:
                            p_count += 1
                        elif i in neg:
                            n_count += 1
                    # Ignore sentences which contain positive and negative words
                    if p_count > 0 and n_count > 0:
                        continue
                    elif p_count > 0:
                        ps_count += 1
                    elif n_count > 0:
                        # Two negative words in one sentence could be a positive sentence
                        if n_count == 2:
                            ps_count += 1
                        else:
                            ns_count += 1
                # Zero our counters
                p_count = 0
                n_count = 0
    # Preventing ZeroDivisionError
    try:
        a = round(ps_count/ns_count, 4)
    except ZeroDivisionError:
        a = None
    try:
        b = round(ps_count/count, 4)
    except ZeroDivisionError:
        b = None
    try:
        c = round(ns_count/count, 4)
    except ZeroDivisionError:
        c = None
    return ps_count, ns_count, a, b, c

# Check if it is an Australian, Canadian or British website
def domain_pat(my_url):
    au_flag = 0
    ca_flag = 0
    uk_flag = 0
    # Use 2 splits to get url
    token = my_url.split('://')[1].split('/')[0]
    token = token.replace(':','.').split('.')[-2:]
    if "au" in token:
        au_flag = 1
    elif "ca" in token:
        ca_flag = 1
    elif "uk" in token:
        uk_flag = 1
    # Return flag combination to determine country
    return au_flag, ca_flag, uk_flag

# Comparing how patriotic people are among Australia, Canada and UK
def patriotic(dictionary):
    au_count = 0
    au_words = 0
    ca_count = 0
    ca_words = 0
    uk_count = 0
    uk_words = 0
    for url in dictionary.keys():
        # If people mention Australia on au websites
        if domain_pat(url) == (1, 0, 0):
            au_count += dictionary.get(url).split().count('australia')
            au_words += len(dictionary.get(url).split())
        # If people mention Canada on ca websites
        elif domain_pat(url) == (0, 1, 0):
            ca_count += dictionary.get(url).split().count('canada')
            ca_words += len(dictionary.get(url).split())
        # If people mention UK, United Kingdom or Great Britain on uk websites
        elif domain_pat(url) == (0, 0, 1):
            uk_count += dictionary.get(url).count('united kingdom')
            uk_count += dictionary.get(url).count('great britain')
            uk_count += dictionary.get(url).split().count('uk')
            uk_words += len(dictionary.get(url).split())
    # Preventing ZeroDivisionError
    try:
        au = round(100*au_count/au_words, 4)
    except ZeroDivisionError:
        au = None
    try:
        ca = round(100*ca_count/ca_words, 4)
    except ZeroDivisionError:
        ca = None
    try:
        uk = round(100*uk_count/uk_words, 4)
    except ZeroDivisionError:
        uk = None
    return au, ca, uk

# Count urls all those Australian websites linked to
def link_au(dictionary):
    count = 0
    domain = []
    for url in dictionary.keys():
        if domain_au(url):
            # Split all urls we stored earlier with a space key
            for link in dictionary.get(url).split():
                count = dictionary.get(url).split().count(link)
                # Restore how often the url had been linked to in tuples
                domain.append((link, count))
                count = 0
    # Remove duplicated values
    domain = set(domain)
    # Sort frequency in descending order. If tie, then sorted urls in ascending order
    domain = sorted(domain,key=lambda a:(-a[1],a[0]))
    # Only return the top 5 websites
    return domain[:5]