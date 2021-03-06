import os

dir = os.path.dirname(__file__)


def parse_to_better_csv(raw_data):
    print("convert shitty csv")
    out = open(dir + "/data/lyrics2_0.txt", 'w', encoding='UTF-8')

    sb = raw_data[0]
    song_nr = 1
    for index, line in enumerate(raw_data[1:]):
        if index % 10000 == 0:
            print(index)
        # brave idea: if the line starts with the index+1, a new song began:
        # print(str(song_nr), line[0:6])
        if str(song_nr) in line[0:6]:
            sb += "\n"
            out.writelines(sb)
            sb = line.replace("\n", " codenewline ")
            song_nr += 1
        else:
            sb += line.replace("\n", " codenewline ")
    return sb


def __load_sp_data__(file, n=-1):
    if n == -1:
        data = open(dir + "/data/" + file, 'r', encoding='UTF-8').readlines()
    else:
        data = open(dir + "/data/" + file, 'r', encoding='UTF-8').readlines()[0:n+1]
    bl = [line.replace("\n", "") for line in open(dir + "/data/blacklist_genre.txt", 'r', encoding='UTF-8').readlines()]
    df = []
    for line in data[1:]:
        try:
            index = line[0:line.index(",")]
            line = line.replace(line[0:line.index(",")+1], "")
            song = line[0:line.index(",")]
            line = line.replace(line[0:line.index(",") + 1], "")
            year = line[0:line.index(",")]
            line = line.replace(line[0:line.index(",") + 1], "")
            artist = line[0:line.index(",")]
            line = line.replace(line[0:line.index(",") + 1], "")
            genre = line[0:line.index(",")]
            if genre in bl:
                continue
            line = line.replace(line[0:line.index(",") + 1], "")
            lyrics = line.replace("\n", "")
            if len(lyrics.replace("codenewline", "").split(" ")) < 5:
                continue
            entry = {'index': index
                     , 'song': song
                     , 'year': year
                     , 'artist': artist
                     , 'genre': genre
                     , 'lyrics': lyrics}
            df.append(entry)
        except:
            print("An unexpected error occured. Skipped that line.")
            # print(line, len(df))
        # print(index, ";", song, ";", year, ";", artist, ";", genre, ";", lyrics)
    return df


def load_data():
    return __load_sp_data__("lyrics2_0.txt")


def load_clean_data(n=-1):
    if n == -1:
        return __load_sp_data__("lyrics3_0.txt")
    else:
        return __load_sp_data__("lyrics3_0.txt", n=n)


def load_balanced_data():
    return __load_sp_data__("lyrics3_0_balanced.txt")


def load_balanced_genre_data():
    return __load_sp_data__("lyrics3_0_balanced_genre.txt")

def balance_data():
    data = load_clean_data()
    # divide data by year:
    old = [d for d in data if int(d['year']) < 2000]
    new = [d for d in data if int(d['year']) >= 2000]
    samplesize = min(1000, len(old), len(new))
    import random
    random.shuffle(new)
    random.shuffle(old)
    new = new[0:samplesize]
    old = old[0:samplesize]
    # save the new data set:
    out = open("data/lyrics3_0_balanced.txt", 'w')
    for entry in old:
        out.write(entry['index'] + "," + entry['song'] + "," + entry['year'] + "," + entry['artist'] + "," + entry[
            'genre'] + "," + entry['lyrics'] + "\n")
    for entry in new:
        out.write(entry['index'] + "," + entry['song'] + "," + entry['year'] + "," + entry['artist'] + "," + entry[
            'genre'] + "," + entry['lyrics'] + "\n")

    print(old[0])

def balance_data_genre():
    data = load_clean_data()
    # divide data by year:
    print(data[0])
    rock = [d for d in data if d['genre'] == "Rock"]
    pop = [d for d in data if d['genre'] == "Pop"]
    hiphop = [d for d in data if d['genre'] == "Hip-Hop"]
    metal = [d for d in data if d['genre'] == "Metal"]

    samplesize = min(500, len(rock), len(pop))

    import random
    random.shuffle(rock)
    random.shuffle(pop)
    random.shuffle(hiphop)
    random.shuffle(metal)

    rock = rock[0:samplesize]
    pop = pop[0:samplesize]
    hiphop = hiphop[0:samplesize]
    metal = metal[0:samplesize]

    # save the new data set:
    out = open("data/lyrics3_0_balanced_genre.txt", 'w')
    for entry in pop:
        out.write(entry['index'] + "," + entry['song'] + "," + entry['year'] + "," + entry['artist'] + "," + entry[
            'genre'] + "," + entry['lyrics'] + "\n")
    for entry in rock:
        out.write(entry['index'] + "," + entry['song'] + "," + entry['year'] + "," + entry['artist'] + "," + entry[
            'genre'] + "," + entry['lyrics'] + "\n")
    for entry in hiphop:
        out.write(entry['index'] + "," + entry['song'] + "," + entry['year'] + "," + entry['artist'] + "," + entry[
            'genre'] + "," + entry['lyrics'] + "\n")
    for entry in metal:
        out.write(entry['index'] + "," + entry['song'] + "," + entry['year'] + "," + entry['artist'] + "," + entry[
            'genre'] + "," + entry['lyrics'] + "\n")

    print(pop[0])

if __name__ == '__main__':
    # raw_data = open(dir + "/data/lyrics.csv", 'r', encoding='UTF-8').readlines()
    # load_data()
    msg = """
    load this file to get a dataframe of all songs in the database. The dataframe (df) is an array of dictionaries,
    each dictionary looks like this:
    dictionary = {'index': index
                 , 'song': song
                 , 'year': year
                 , 'artist': artist
                 , 'genre': genre
                 , 'lyrics': lyrics}
    Access the attributes with the keys, like df[0]['lyrics'] to get the lyrics of the first song.
    """
    print(msg)
    # print(parse_to_better_csv(open(dir + "/data/lyrics.csv", 'r', encoding='UTF-8'). readlines()))
    balance_data_genre()




