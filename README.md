# CCM_FinalProject Christopher Strucks, Tristan Payer

## Study Proposal
It came to our ears that modern song lyrics are said to uncreative. The goal of our study is to give an overview about the creativity of modern songs (songs later than 2000) versus old songs (before 2000). According to Mumford (2003), "creativity involves the production of novel, useful products". Based on this definition and on several creativity tests (Guilford's Test of Divergent Thinking (1967), ... ) we will define creativity metrics to compare old song lyrics and new song lyrics. Further we want to investigate if there is a significant difference between song genres in terms of creativity.

To archive that, we will use the Metro Lyrics data published on Kaggle (https://www.kaggle.com/gyani95/380000-lyrics-from-metrolyrics/data), which comprises more than 380.000 songs of various artists. For every song we will extract the creativity features described below. For topic extraction we will use TextRank, which was developed by Rada Mihalcea and Paul Tarau in 2012 and it basically exploits the structure of a text to find central key phrases. This algorithm is inspired by the PageRank algorithm, which is an unsupervised algorithm to determine the importance of web pages. Alternatively, we could use the tf-idf score to determine the importance of certain words for a text. The tf-idf (term frequency - inverse document frequency) assigns every word in a "document" (in this project "song") a numerical score that reflects how important a word is for the document in the collection of documents. This method was first introduced by Karen Spärck Jones in 1972.

Not sure how we can evaluate the data, we suggest:
* a simple MANOVA to see which factors are significantly different in the old vs modern comparison.
* train a Random Forest to determine which features are important.
* train a classifier (SVM, logistic regression, ect) and see how it performs (if it performs bad, the data cannot be separated and thus there is no difference in creativity)
* clustering analysis
* simple plots of subspaces
* combine features into one creativity score and do a simple t-test


This evaluation would be the same for the creativity difference between genres. (Maybe logistic regression)

## TODO
* finalize preprocessing
* do data exploration
* implement everything
* ranking of most creative genres
* correlation between success and creativity (? if time is left)

## Creativity measures:
* number unique words across song (higher better) ✔️
* number unique words across artist (higher better) ✔️
* number unique words across genre (higher better) ✔️
* average rhyme length (higher better)
* number filler words (eg. "Ohh", "Yeah", "Baby", "Uhh", "Ahh") (lower better)
* number of topics across song (maybe TextRank or tf Idf, LDA) (maybe take this out)
* number topics across artist (higher better)

## Needs
* Lyrics DB (artist, year, lyrics, genre)
* Phoneme DB
* Success DB (only if time left)

## References:
Mumford, M. D. (2003). "Where have we been, where are we going? Taking stock in creativity research". Creativity Research Journal. 15: 107–120. doi:10.1080/10400419.2003.9651403.

Guilford, J. P. (1967). Creativity: Yesterday, today and tomorrow. The Journal of Creative Behavior, 1(1), 3-14.

Mihalcea, R., & Tarau, P. (2004). Textrank: Bringing order into text. In Proceedings of the 2004 conference on empirical methods in natural language processing.

Sparck Jones, K. (1972). A statistical interpretation of term specificity and its application in retrieval. Journal of documentation, 28(1), 11-21.
