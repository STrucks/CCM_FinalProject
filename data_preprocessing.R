library(dplyr)
library(textcat)
library(tidyr)
library(tidytext)
library(stringr)


# TODO: look again over the filtering of the data.
# watch for: year, language, strange artist(just numbers, just one song, too many songs), duplicate artists(beyonce = beyonce-knowles)
data <- read.csv("../lyrics.csv")

# remove outlier years
data <- data %>%
  filter(lyrics != "") #%>%
  # for some reson the language detection does not work anymore
  #filter(textcat(lyrics) == "english" |textcat(lyrics) == "scots")


# remove things like [verse:], [chorus:]
data$lyrics <- gsub("\\[[^\\]]*\\]", "", data$lyrics, perl=TRUE)

# remove non ASCII characters:
data$lyrics <- iconv(data$lyrics, "latin1", "ASCII", sub="")

# Put data in tidy format to make it easier to work with
tidy_data <- data %>%
  unnest_tokens(word, lyrics)

# get song distibutions accross year
year <- data %>%
  count(year, sort = TRUE) %>%
  filter(year > 1900 & year < 2018)

# get song distribution accross the differnt genres
genre <- data %>%
  count(genre, sort = TRUE)

# plot the number of songs per genre
barplot(genre$n, names.arg = genre$genre, main = "Number of songs per genre")

# number of songs per artist
songs_per_artist <- data %>%
  count(artist)


#############################################################################
#                   Descriptive statistics from the Readme                  #
#############################################################################

# get the number of words and unique words per song
num_words_song <- tidy_data %>%
  group_by(song)%>%
  summarise(num_words = n(), num_unique_words = n_distinct(word)) %>%
  mutate(per_unique = num_unique_words/num_words)
  
# get mean and sd for num of words per song
mean_num_words_song <- mean(num_words_song$num_words)
stdev_num_words_song <- sd(num_words_song$num_words)

# count the number of unique words per artist
num_words_artist <- tidy_data %>%
  group_by(artist) %>%
  summarise(num_words = n(), num_unique_words = n_distinct(word)) %>%
  mutate(per_unique = num_unique_words/num_words)

# get mean and sd for artists
mean_num_words_artist <- mean(num_words_artist$num_words)
stdev_num_words_artist <- sd(num_words_artist$num_words)

# count the number of unique words per genre 
num_words_genre <- tidy_data %>%
  group_by(genre) %>%
  summarise(num_words = n(), num_unique_words = n_distinct(word)) %>%
  mutate(per_unique = num_unique_words/num_words)

# get mean and sd for genre
mean_num_words_genre <- mean(num_words_genre$num_words)
stdev_num_words_genre <- sd(num_words_genre$num_words)

