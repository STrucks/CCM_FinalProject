import matplotlib.pyplot as plt
import numpy as np

def train(features, labels):
    print("start training")
    from sklearn.model_selection import cross_val_score
    # from sklearn import svm
    # model = svm.SVC(kernel='rbf')
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(max_depth=2)
    print("start CV")
    scores = cross_val_score(model, features, labels, cv=10)
    print(scores)
    print(sum(scores) / (len(scores)))
    return sum(scores) / (len(scores))


def plot(data, x, y, labels):
    colors = ['green', 'r', 'b', 'y', 'orange']
    label_index = list(set(labels))
    for i, row in enumerate(data):
        plt.plot(float(row[x]), float(row[y]), 'x', color=colors[label_index.index(labels[i])], label=labels[i])
    plt.xlabel("index of song")
    plt.ylabel("total number of words")
    plt.gca().legend(label_index)
    plt.show()


def load_features(data):
    word_dict = {}
    w_index = 0
    for line in data:
        if line[3] not in word_dict:
            word_dict[line[3]] = w_index
            w_index += 1
        if line[5] not in word_dict:
            word_dict[line[5]] = w_index
            w_index += 1
        if line[7] not in word_dict:
            word_dict[line[7]] = w_index
            w_index += 1
    print(len(word_dict), word_dict)
    print(data)
    features = []
    for index, line in enumerate(data):
        row = []
        if line[4] != "":  # top 1 tfidf score
            row.append(float(line[4]))
        else:
            row.append(0)
        if line[6] != "":  # top 2 tfidf score
            row.append(float(line[6]))
        else:
            row.append(0)
        if line[8] != "":  # top 3 tfidf score
            row.append(float(line[8]))
        else:
            row.append(0)
        row += [sum(row[0:3]) / 3]
        if line[9] != "":  # number words
            row.append(float(line[9]))
        else:
            row.append(0)
        if line[10] != "":  # number unique words
            row.append(float(line[10]))
        else:
            row.append(0)
        if line[11] != "":  # ration unique words
            row.append(float(line[11]))
        else:
            row.append(0)
        if line[12] != "":  # number of rhymes
            row.append(float(line[12]))
        else:
            row.append(0)
        if line[13] != "":  # total words of artist
            row.append(float(line[13]))
        else:
            row.append(0)
        if line[14] != "":  # number unique words of artist
            row.append(float(line[14]))
        else:
            row.append(0)
        if line[15] != "":  # artist (index)
            row.append(0)
        else:
            row.append(0)
        if line[16] != "":  # year
            row.append(float(line[16]))
        else:
            row.append(0)

        row += [word_dict[line[3]], word_dict[line[5]], word_dict[line[7]]]
        # row += [float(n) for n in unigram[index]]

        features.append(row)
    return features


def load_baby():
    data = [line.replace("\n", "").split(",")[-2:] for line in open("data/conc_and_baby.csv", 'r').readlines()[1:]]
    data = [[float(d[0]), float(d[1])] for d in data]
    return data

def load_rake():
    data = [line.replace("\n", "").split(",")[1:] for line in open("data/rakeResults.csv", 'r').readlines()[1:]]
    word_dict = {}
    w_index = 0
    for line in data:
        words = line[1].split(" ")
        for w in words:
            if w not in word_dict:
                word_dict[w.replace("\"", "")] = w_index
                w_index += 1
    songs = [line.replace("\n", "").replace("\"", "").split(",")[2] for line in open("data/conc_and_baby.csv", 'r').readlines()[1:]]
    features = []
    for song in songs:
        f_row = []
        # print(song, [line[0].replace("\"", "") for line in data])
        words = [line[1].replace("\"", "").split(" ") for line in data if line[0].replace("\"", "") == song]
        for row in words:
            for w in row:
                if w == 'codenewline':
                    continue
                f_row.append(word_dict[w])
        if len(f_row) < 10:
            features.append(f_row + [0]*(10-len(f_row)))
        elif len(f_row) > 10:
            features.append(f_row[0:10])
        else:
            features.append(f_row)
    print("f", features)
    return features



if __name__ == '__main__':
    # first import all the features:
    data = [line.replace("\n", "").split(";") for line in open("data/merged_genre.csv", 'r').readlines()]
    features1 = load_features(data)
    features2 = load_baby()
    features3 = load_rake()
    print(np.average(features3))
    features = []
    for i in range(len(features1)):
        features.append(features1[i] + features2[i] + features3[i])

    print(features)
    # labels = [1 if int(line[1]) >= 2000 else 0 for line in data]
    labels = [d[2] for d in data]

    """
    0 = top 1 tfidf score
    1 = top 2 tfidf score
    2 = top 3 tfidf score
    3 = avg tfidf
    4 = number words
    5 = number unique words
    6 = ration unique words
    7 = number of rhymes
    8 = total words of artist
    9 = number unique words of artist
    10 = artist (index)
    11 = year
    12 = best tf-idf word (index)
    13 = second best tf-idf word (index)
    14 = third best tf-idf word (index)
    15 = sum_babyness
    16 = sum_conc
    17 - 27 = rake words
    """

    print([row[9] for row in features])

    # feature selection:
    remove = range(15)
    perf = []
    LABELS = ["tf-idf scores", "#words", "#rhymes", "#wordsOfArtist", "year", "tf-idf words", "babyness", "conc", "rake", "baseline"]
    for trial in range(10):
        p = []
        sel_features = [row[4:] for row in features]
        p.append(train(sel_features, labels))
        sel_features = [row[0:4] + row[7:] for row in features]
        p.append(train(sel_features, labels))
        sel_features = [row[0:7] + row[8:] for row in features]
        p.append(train(sel_features, labels))
        sel_features = [row[0:8] + row[11:] for row in features]
        p.append(train(sel_features, labels))
        sel_features = [row[0:11] + row[12:] for row in features]
        p.append(train(sel_features, labels))
        sel_features = [row[0:12] + row[15:] for row in features]
        p.append(train(sel_features, labels))
        sel_features = [row[0:15] + row[16:] for row in features]
        p.append(train(sel_features, labels))
        sel_features = [row[0:16] + row[17:] for row in features]
        p.append(train(sel_features, labels))
        sel_features = [row[0:17] for row in features]
        p.append(train(sel_features, labels))

        p.append(train(features, labels))
        perf.append(p)
    perf = np.mean(perf, axis=0)
    plt.bar(range(len(perf)), perf)
    plt.xticks(range(len(perf)), LABELS)
    plt.show()
    plt.figure(1)
    plt.bar(range(len(perf)), perf - perf[-1])
    plt.xticks(range(len(perf)), LABELS)
    plt.show()

    """
    perf = []
    for trial in range(10):
        p = []
        for r in remove:
            sel_features = [[row[r]] for row in features]
            p.append(train(sel_features, labels))
        p.append(train(features, labels))
        perf.append(p)
    perf = np.mean(perf, axis=0)
    plt.plot(range(16), perf)
    plt.show()
    """


    """
    Feature Analysis:
    with all features:      88%
    no artist:              53%
    
    """



