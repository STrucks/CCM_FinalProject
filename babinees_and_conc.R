library(dplyr)
library(textcat)
library(tidyr)
library(tidytext)
library(stringr)

# read song texts
#balanced <- read.csv("lyrics3_0_balanced_genre.txt", header = FALSE, col.names = c("index", "song", "year", "artist", "genre", "lyrics"),
#                     colClasses = c("integer", "character", "integer", "character", "character", "character"))

# converte to tidy format. takes long, possible already done before
#tidy_balanced <- balanced %>%
#  unnest_tokens(word, lyrics)

# read and preprocess babness ratings
babiness <- read.csv("./babiness.txt") %>%
  select(word, babyAVG)
babiness$word <- as.character(babiness$word)

babiness <- babiness %>%
  group_by(word) %>%
  summarise(avg = mean(babyAVG))

# read and preprocess concreteness ratings
concreteness <- read.csv("./word_concreteness.txt", sep = "\t") %>%
  select(Word, Conc.M)
colnames(concreteness)[1] <- "word"
concreteness$word <- as.character(concreteness$word)

tidy_balanced <- tidy_balanced %>%
  left_join(babiness) %>%
  left_join(concreteness)

# rename columns
colnames(tidy_balanced)[7] <- "babiness"
colnames(tidy_balanced)[8] <- "concreteness" 


# compute sum of babiness and concreteness per song

tidy_balanced <- tidy_balanced %>%
  group_by(song) %>%
  summarise(sum_babiness=sum(babiness, na.rm = T), sum_conc=sum(concreteness, na.rm = T))

# write as .csv
write.csv(tidy_balanced, "./conc_and_baby.csv")
