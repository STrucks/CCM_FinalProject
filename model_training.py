

if __name__ == '__main__':
    # first import all the features:
    data = [line.replace("\n", "").split(";") for line in open("data/merged.csv", 'r').readlines()]
    unigram = [line.replace("\n", "").split(";") for line in open("data/features.txt", 'r').readlines()]
    print(data)
    features = []
    for index, line in enumerate(data):
        row = []
        if line[4] != "":
            row.append(float(line[4]))
        else:
            row.append(0)
        if line[6] != "":
            row.append(float(line[6]))
        else:
            row.append(0)
        if line[8] != "":
            row.append(float(line[8]))
        else:
            row.append(0)
        row += [sum(row[0:3])/3, float(line[9]), float(line[10]), float(line[11])]
        row += [float(n) for n in unigram[index]]
        features.append(row)
    labels = [1 if int(line[1]) >= 2000 else 0 for line in data]
    print("start training")
    from sklearn import svm
    from sklearn.model_selection import cross_val_score
    #model = svm.SVC(kernel='rbf')
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(max_depth=2)
    print("start CV")
    scores = cross_val_score(model, features, labels, cv=10)
    print(scores)
    print(sum(scores)/(len(scores)))
