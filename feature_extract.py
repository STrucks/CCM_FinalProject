import import_data
import time
import math
from textblob import TextBlob as tb

def extract(data):
    out = open("data/features.txt", 'w')
    # load and format the phonemes db:
    phonemes_db = open("data/dictionary.txt", 'r').readlines()
    _data_ = []
    for line in phonemes_db:
        line = line.replace("\n", "")
        word = ""
        for i, c in enumerate(line):
            if c == " " and line[i + 1] == " ":
                continue
            elif c == " ":
                word += ";"
            else:
                word += c
        words = word.split(";")
        ph = " ".join(words[2:])
        _data_.append([words[0].lower(), ph])

    phonemes_db = _data_

    artists = {}
    for entry in data:
        if entry['artist'] not in artists:
            artists[entry['artist']] = entry['lyrics'].replace("\"", "").replace(" codenewline", "")
        else:
            artists[entry['artist']] += " " + entry['lyrics'].replace("\"", "").replace(" codenewline", "")

    # start feature extraction:
    features = []
    for entry in data:
        row = []
        entry['lyrics'] = entry['lyrics'].replace("\"", "")
        lyrics = entry['lyrics']
        lyrics.replace(" codenewline", "")
        # number unique words:
        words = lyrics.split(" ")
        unique_words = len(set(words))
        row.append(str(unique_words))
        # proportion unique words:
        prop_unique_words = len(set(words))/len(words)
        row.append(str(prop_unique_words))
        """
        # rhymes:
        rhyme_score = 0
        song_lines = entry['lyrics'].split(" codenewline ")
        for line in range(len(song_lines)):
            # look up how much this line rhymes with the next one:
            cur_line = song_lines[line].split(" ")
            if line+1 < len(song_lines):
                next_line = song_lines[line+1].split(" ")
            else:
                continue
            min_line_length = min(len(cur_line), len(next_line), 5)
            phonemes_line1 = []
            phonemes_line2 = []

            for w in range(min_line_length):
                w1 = cur_line[-(w+1)]
                w2 = next_line[-(w+1)]
                ph1 = [p for word, p in phonemes_db if word == w1]
                ph2 = [p for word, p in phonemes_db if word == w2]
                if ph1 == [] or ph2 == []:
                    continue
                else:
                    ph1 = ph1[0]
                    ph2 = ph2[0]
                phonemes_line1 += ph1.split(" ")
                phonemes_line2 += ph2.split(" ")

            min_phon_length = min(len(phonemes_line1), len(phonemes_line2), 5)

            for p in range(min_phon_length):
                if phonemes_line1[-(p+1)] == phonemes_line2[-(p+1)]:
                    rhyme_score += 1

            #print(rhyme_score)
        print(";".join(row))
        row.append(str(rhyme_score))
        """
        # total words of a artist:
        row.append(str(len(artists[entry['artist']].split(" "))))
        # unique words across artist:
        row.append(str(len(set(artists[entry['artist']].split(" ")))))
        # unique words in that song:






        print(row)
        out.write(str(entry['index']) + ";" + ";".join(row) + "\n")
        features.append(row)



    print(features)
    return features

def tf_idf(data):
    out = open("data/features.txt", 'w')
    features = []
    bloblist = []
    for entry in data:
        row = []
        entry['lyrics'] = entry['lyrics'].replace("\"", "")
        lyrics = entry['lyrics']
        lyrics.replace(" codenewline", "")
        bloblist.append(tb(lyrics))

    for i, blob in enumerate(bloblist):
        print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        out.write(data[i]['index'])
        for word, score in sorted_words[:3]:
            print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
            out.write(";" + word + ";" + str(round(score, 5)))
        out.write("\n")

idfs = {}

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


def idf(word, bloblist):
    if word in idfs:
        return idfs[word]
    else:
        idfs[word] = math.log(len(bloblist) / (1 + n_containing(word, bloblist)))
        return idfs[word]
"""
def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))
"""
def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


if __name__ == '__main__':
    t0 = time.clock()
    df = import_data.load_balanced_data()
    print(time.clock() - t0)
    t0 = time.clock()
    tf_idf(df)
    print(time.clock() - t0)
