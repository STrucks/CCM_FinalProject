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
            sb = line.replace("\n", " ")
            song_nr += 1
        else:
            sb += line.replace("\n", " ")
        """
        if len(line) <= 3:
            sb += line.replace("\n", " ")
        elif line[-1] == "\n" and line[-2] == "\"" and line[-3] != "\"":
            sb += line
            out.writelines(sb)
            sb = ""
        else:
            sb += line.replace("\n", " ")
        """
    return sb


def __load_sp_data__(file):
    data = open(dir + "/data/" + file, 'r', encoding='UTF-8').readlines()
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
            line = line.replace(line[0:line.index(",") + 1], "")
            lyrics = line.replace("\n", "")
            entry = {'index': index
                     , 'song': song
                     , 'year': year
                     , 'artist': artist
                     , 'genre': genre
                     , 'lyrics': lyrics}
            df.append(entry)
        except:
            print("An unexpected error occured. Skipped that line.")
            print(line, len(df))
        # print(index, ";", song, ";", year, ";", artist, ";", genre, ";", lyrics)
    return df


def load_data():
    return __load_sp_data__("lyrics2_0.txt")


def load_clean_data():
    return __load_sp_data__("lyrics3_0.txt")

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
    print(parse_to_better_csv(open(dir + "/data/lyrics.csv", 'r', encoding='UTF-8'). readlines()))


