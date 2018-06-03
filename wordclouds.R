library(dplyr)
library(wordcloud)
library(RColorBrewer) 

pal <- brewer.pal(8,"Spectral")
wordcloud <- tidy_data %>%
  anti_join(stop_words) %>%
  count(word) %>%
  with(wordcloud(word, n, max.words = 100, scale = c(4,.9), random.color=T, colors = pal))

for(genre in genres){
  # make room for the title and add title to plot
  layout(matrix(c(1, 2), nrow=2), heights=c(1, 4))
  par(mar=rep(0, 4))
  plot.new()
  text(x=0.5, y=0.5, genre)
  
  # add actiul wordcloud to plot
  wordcloud <- tidy_data %>%
    anti_join(stop_words) %>%
    filter(genre == genre) %>%
    count(word) %>%
    with(wordcloud(word, n, max.words = 100, scale = c(4,.9), random.color=T, colors = pal))
  
  #TODO: save plots
}
