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


if __name__ == '__main__':
    # first import all the features:
    data = [line.replace("\n", "").split(";") for line in open("data/merged_genre.csv", 'r').readlines()]
    #unigram = [line.replace("\n", "").split(";") for line in open("data/features.txt", 'r').readlines()]
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
        if line[4] != "": # top 1 tfidf score
            row.append(float(line[4]))
        else:
            row.append(0)
        if line[6] != "": # top 2 tfidf score
            row.append(float(line[6]))
        else:
            row.append(0)
        if line[8] != "": # top 3 tfidf score
            row.append(float(line[8]))
        else:
            row.append(0)
        if line[9] != "": # number words
            row.append(float(line[9]))
        else:
            row.append(0)
        if line[10] != "": # number unique words
            row.append(float(line[10]))
        else:
            row.append(0)
        if line[11] != "": # ration unique words
            row.append(float(line[11]))
        else:
            row.append(0)
        if line[12] != "": # number of rhymes
            row.append(float(line[12]))
        else:
            row.append(0)
        if line[13] != "": # total words of artist
            row.append(float(line[13]))
        else:
            row.append(0)
        if line[14] != "": # number unique words of artist
            row.append(float(line[14]))
        else:
            row.append(0)
        if line[15] != "": # artist (index)
            row.append(float(line[15]))
        else:
            row.append(0)
        if line[16] != "": # year
            row.append(float(line[16]))
        else:
            row.append(0)

        row += [sum(row[0:3])/3]
        row += [word_dict[line[3]], word_dict[line[5]], word_dict[line[7]]]
        #row += [float(n) for n in unigram[index]]

        features.append(row)

    # labels = [1 if int(line[1]) >= 2000 else 0 for line in data]
    labels = [d[2] for d in data]

    """
    0 = top 1 tfidf score
    1 = top 2 tfidf score
    2 = top 3 tfidf score
    3 = number words
    4 = number unique words
    5 = ration unique words
    6 = number of rhymes
    7 = total words of artist
    8 = number unique words of artist
    9 = artist (index)
    10 = year
    11 = avg tfidf
    12 = best tf-idf word (index)
    13 = second best tf-idf word (index)
    14 = third best tf-idf word (index)
    """

    print([row[9] for row in features])

    # feature selection:
    remove = range(15)
    perf = []
    for trial in range(10):
        p = []
        for r in remove:
            sel_features = [row[0:r] + row[r + 1:] for row in features]
            p.append(train(sel_features, labels))
        p.append(train(features, labels))
        perf.append(p)
    perf = np.mean(perf, axis=0)
    plt.plot(range(16), perf)
    plt.show()
    plt.figure(1)
    plt.bar(range(16), perf - perf[-1])
    plt.show()

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
    Feature Analysis:
    with all features:      88%
    no artist:              53%
    
    """



