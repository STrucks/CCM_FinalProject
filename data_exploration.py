import import_data

import matplotlib.pyplot as plt


"""
Data exploration:

Artists:
run the code

Genres:
{'Pop': 40437, 'Hip-Hop': 24823, 'Not Available': 23908, 'Rock': 109147, 'Metal': 23694, 'Other': 5183, 'Country': 14384,
 'Jazz': 7971, 'Electronic': 7959, 'Folk': 2242, 'R&B': 3399, 'Indie': 3148, '"': 2}

Year distribution:
67: 1           removed
112: 4          removed
702: 1          removed
1968: 1
1970: 172
1971: 199
1972: 192
1973: 246
1974: 161
1975: 146
1976: 82
1977: 256
1978: 189
1979: 187
1980: 203
1981: 188
1982: 246
1983: 147
1984: 181
1985: 174
1986: 190
1987: 127
1988: 194
1989: 264
1990: 1139
1991: 307
1992: 642
1993: 568
1994: 606
1995: 739
1996: 771
1997: 779
1998: 813
1999: 1038
2000: 1202
2001: 1212
2002: 1530
2003: 1718
2004: 2719
2005: 4642
2006: 74193
2007: 62480
2008: 19588
2009: 10174
2010: 9739
2011: 9829
2012: 11290
2013: 10822
2014: 12759
2015: 10151
2016: 11096

"""




if __name__ == '__main__':
    df = import_data.load_clean_data()
    # there are some mistakes in the data, I fixed some of them by hand. (These mistakes were not produced by the preprocessing, eg. no artist, ect)
    # show basic stats: amount of songs per artist, genre, time (before 2000 and after)
    nr_song_artist = {}
    nr_song_genre = {}
    nr_song_year = {}

    for entry in df:
        if entry['artist'] not in nr_song_artist:
            nr_song_artist[entry['artist']] = 1
        else:
            nr_song_artist[entry['artist']] += 1

        if entry['genre'] not in nr_song_genre:
            nr_song_genre[entry['genre']] = 1
        else:
            nr_song_genre[entry['genre']] += 1

        if entry['year'] not in nr_song_year:
            nr_song_year[(entry['year'])] = 1
        else:
            nr_song_year[(entry['year'])] += 1

    # print(nr_song_artist)
    # print(nr_song_genre)
    sorted_years = []
    sorted_keys = []
    for key in sorted(nr_song_year):
        sorted_years.append(nr_song_year[key])
        sorted_keys.append(key)
    plt.bar(sorted_keys, sorted_years)
    plt.show()

    # find a good balance old vs new:
    boarder = 2000
    nr_old = 0
    nr_new = 0
    for key in nr_song_year:
        if int(key) < boarder:
            nr_old += nr_song_year[key]
        else:
            nr_new += nr_song_year[key]
    print("old:", nr_old, "new:", nr_new, "ratio:", nr_old/nr_new, "% new:", nr_new/(nr_new+nr_old), "% old:", nr_old/(nr_new+nr_old))

    # a good balance between old and new is not possible, since % old if boarder = 2008: 60% and if boarder = 2007: 37%
    # i guess we go for a subset of the new songs from 2000 onwards

    # plt.bar([key for key in nr_song_genre], [nr_song_genre[key] for key in nr_song_genre])
    # plt.show()






