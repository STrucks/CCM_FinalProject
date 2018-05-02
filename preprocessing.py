import import_data
dir = import_data.dir

"""
Preprocess the song data:
-> clean data 
    |
    -> remove char like !?+.,:;-_<>&%()'"[]
    |
    -> remove non english songs
    |
    -> remove tags like [chorous], [artist], ect
    |
    -> make it all lowercase

"""



def is_ascii(c):
    return ord(c) < 128



def clean_data(df):
    invalid_chars = "!?+.,:;-_<>&%()[]\'\""
    invalid_lyrics = [" ", "", "  "]
    print(len(df))
    invalid_entries = []
    invalid_entries = []
    for i, entry in enumerate(df):
        if i % 10000 == 0:
            print(i)
        lyrics = entry['lyrics']
        if lyrics in invalid_lyrics:
            continue
        # make it all lowercase
        lyrics = lyrics.lower()
        # remove tags
        while lyrics.find("[") >= 0:
            start = lyrics.find("[")
            end = lyrics.find("]")
            if start > end:
                break
            substr = lyrics[start:end+2]
            lyrics = lyrics.replace(substr, "")
        # remove invalid characters:

        for c in lyrics:
            if c in invalid_chars:
                lyrics = lyrics.replace(c, "")
            elif not is_ascii(c):
                lyrics = lyrics.replace(c, "")

        

        # remove double spaces or triple spaces:
        lyrics = lyrics.replace("   ", " ")
        lyrics = lyrics.replace("  ", " ")
        entry['lyrics'] = lyrics
        invalid_entries.append(entry)


    # write clean data to lyrics3_0.txt
    print("write to file")
    out = open(dir + "/data/lyrics3_0.txt", 'w', encoding='UTF-8')
    out.write("index,song,year,artist,genre,lyrics\n")
    for entry in invalid_entries:
        sb = entry['index'] + "," + entry['song'] + "," + entry['year'] + "," + entry['artist'] + "," + entry['genre'] + ",\"" + entry['lyrics'] + "\"\n"
        out.write(sb)



if __name__ == '__main__':
    df = import_data.load_data()
    clean_data(df)
    # df = import_data.load_clean_data()

    # print(df[0:10])

