library(slowraker)
library(dplyr)
library(textcat)
library(tidyr)
library(tidytext)
library(stringr)


# Read the dataset
balanced <- read.csv("lyrics3_0_balanced_genre.txt", header = FALSE, col.names = c("index", "song", "year", "artist", "genre", "lyrics"),
                     colClasses = c("integer", "character", "integer", "character", "character", "character"))

# converte to tidy format. takes long, possible already done before
#tidy_balanced <- balanced %>%
#  unnest_tokens(word, lyrics)

# extract key words using RAKE (rapid keyword extraktion)
key_balanced <- slowrake(txt=balanced$lyrics)
rake_results <- rbind_rakelist(key_balanced, doc_id = balanced$song)
colnames(rake_results)[1] <- "song"

#only take the top 5 keywords
rake_results_ <- rake_results %>%
  group_by(song) %>%
  do(head(., n = 5))

# add results to the input
balanced <- balanced %>%
  left_join(rake_results_)

# write as .csv
write.csv(balanced, "./rakeResults.csv")
