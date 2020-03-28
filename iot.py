from googlesearch import search
import bs4 as bs
import urllib.request
import re
import nltk

with open("trusted.txt", "r") as myfile:
    trusted = list(myfile.readlines())
for i in  range(len(trusted)):
    trusted[i] = trusted[i][:len(trusted[i])-1]

with open("spam.txt", "r") as myfile:
    spam = list(myfile.readlines())
for i in  range(len(spam)):
    spam[i] = spam[i][:len(spam[i])-1]


def make_notes_for_article(url):
    try:
        scraped_data = urllib.request.urlopen(url)
    except Exception as HTTPError:
        return
    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article,'lxml')

    paragraphs = parsed_article.find_all('p')

    article_text = ""

    for p in paragraphs:
        article_text += p.text


    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)


    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)


    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    try:
        maximum_frequncy = max(word_frequencies.values())
    except Exception as ValueError:
        pass

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)



    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]


    import heapq
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    print(summary)
    l = list(url.split("."))
    while True:
        if l[1] in trusted:
            break
        add_to_spam = input("Add to Spam Websites (y/n)")
        if add_to_spam!= 'y' and add_to_spam!= 'Y' and add_to_spam!= 'n' and add_to_spam!= 'N' :
            print("Enter a correct Input.\n")
        elif add_to_spam =='y' or add_to_spam =='Y':
            with open("spam.txt", "a") as myfile:
                if len(l[1]) < 4:
                    l[1] = l[2]
                myfile.write(l[1])
                myfile.write("\n")
                spam.append(l[1])
                return
                break
        else:
            break

    while True:
        if l[1] in trusted:
            break
        add_to_trusted = input("Add to Trusted Websites (y/n)")
        if add_to_trusted!= 'y' and add_to_trusted!= 'Y' and add_to_trusted!= 'n' and add_to_trusted!= 'N' :
            print("Enter a correct Input.\n")
        elif add_to_trusted =='y' or add_to_trusted =='Y':
            l = list(url.split("."))
            with open("trusted.txt", "a") as myfile:
                if len(l[1]) < 4:
                    l[1] = l[2]
                myfile.write(l[1])
                myfile.write("\n")
                trusted.append(l[1])
            break
        else:
            break



while 1:
    count = 0
    flag = 0
    query = input("Enter the topic for Preview text :")
    for url in search(query, stop=20):
        if len(url) < 80 :
            for i in spam:
                i = i[:len(i)-1]
                if i  in url:
                    flag = 1
            if  not flag:
                print(url)
                make_notes_for_article(url)
                print('\n\n\n\n')
