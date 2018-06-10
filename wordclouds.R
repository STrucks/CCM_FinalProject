library(dplyr)
library(wordcloud)
library(RColorBrewer) 

pal <- brewer.pal(8,"Spectral")

png(filename = "./imgs/allsong_wc.png", width=12, height=8, units="in", res=300)
wordcloud <- tidy_data %>%
  anti_join(stop_words) %>%
  count(word) %>%
  with(wordcloud(word, n, max.words = 100, scale = c(4,.9), random.color=T, colors = pal))
dev.off()


png(filename = "./imgs/metal_wc.png", width=12, height=8, units="in", res=300)
wordcloud_rock <- tidy_data %>%
  anti_join(stop_words) %>%
  filter(genre=="Metal") %>%
  count(word) %>%
  with(wordcloud(word, n, max.words = 100, scale = c(4,.9), random.color=T, colors = pal))
dev.off()


png(filename = "./imgs/hip_hop_wc.png", width=12, height=8, units="in", res=300)
wordcloud_rock <- tidy_data %>%
  anti_join(stop_words) %>%
  filter(genre=="Hip-Hop") %>%
  count(word) %>%
  with(wordcloud(word, n, max.words = 100, scale = c(4,.9), random.color=T, colors = pal))
dev.off()


# automating the process of creating wordclouds
genres <- unique(data$genre)
for(genre_ in genres){
  # open png device
  png(filename = paste("imgs/", genre_, "_wc.png", sep=""), width=12, height=8, units="in", res=300)
  
  # add actiul wordcloud to plot
  wordcloud <- tidy_data %>%
    anti_join(stop_words) %>%
    filter(genre == genre_) %>%
    count(word) %>%
    with(wordcloud(word, n, max.words = 100, scale = c(4,.9), random.color=T, colors = pal))
  
  # save plots
  dev.off()
}

