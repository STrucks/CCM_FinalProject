import import_data
import time


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
        out.write(str(entry['index']) + ";" + ";".join(row) + "\n")
        features.append(row)

    print(features)
    return features


if __name__ == '__main__':
    t0 = time.clock()
    df = import_data.load_clean_data(n=100)
    print(time.clock() - t0)
    t0 = time.clock()
    extract(df)
    print(time.clock() - t0)
