library(dplyr)
library(textcat)

data <- read.csv("../lyrics.csv")

# remove outlier years
data <- data %>%
  filter(lyrics != "") %>%
  filter(textcat(lyrics) == "english" |textcat(lyrics) == "scots")

# remove things like [verse:], [chorus:]
data$lyrics <- gsub("\\[[^\\]]*\\]", "", data$lyrics, perl=TRUE)

# remove non ASCII characters:
data$lyrics <- iconv(data$lyrics, "latin1", "ASCII", sub="")



year <- data %>%
  count(year, sort = TRUE) %>%
  filter(year > 1900 & year < 2018)

artists <- data %>%
  group_by(artist) %>%
  mutate(mean_year = mean(year))# %>%
  #ungroup()#%>%
  #count(artist, sort = TRUE)

genre <- data %>%
  count(genre, sort = TRUE)
