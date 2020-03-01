# install.packages("devtools")
# library(devtools)
# install.packages(c("tm", "BMS", "quadprog", "rJava", "parallel", "data.table", "entropy"))
# install_github("blogsvoices/iSAX")
# setwd("thesis")

library(iSAX)
library(textstem)
library(pracma)
# usage: iSA(train_data, test_data, train_labels, predict=TRUE)

# TODO: change this string to your state
state <- 'southcarolina'

keywords <- list('bennet', 'biden', 'bloomberg', 'buttigieg', 'gabbard', 'klobuchar', 'patrick', 'sanders', 'steyer', 'warren', 'yang', 'democrat', 'dem', 'caucus', 'primary')
scores <- list()
scores_weighted <- list()

for (word in keywords) {
  print(word)
  train <- read.csv(file = paste('data/', state, '/ceron/all-training-data.csv', sep=""), header=T)
  test <- read.csv(file = paste('data/', state, '/ceron/', word, '_testing_data.csv', sep = ""), header=T)
  train_data<-c(stem_words(train$Word))
  train_labels<-c(stem_words(train$Polarity))
  test_data <- c(stem_words(test$Polarity))

  num <- 0
  denom <- 0
  total <- 0

  results <- iSA(train_data, test_data, train_labels, predict=T)
  preds <- results[6][["pred"]]
  for (sentiment in preds) {
    total <- total + 1
    if (strcmp(sentiment, "weakneg")) {
      denom <- denom + 1
    } else if (strcmp(sentiment, "strongneg")) {
      denom <- denom + 2
    } else if (strcmp(sentiment, "weakpo")) {
      num <- num + 1
    } else if (strcmp(sentiment, "strongpo")) {
      num <- num + 2
    }
  }
  scores[[word]] <- num/denom
  scores_weighted[[word]] <- num/denom*total
}

scores_text <- list()
scores_weighted_text <- list()

i <- 1
for (word in keywords) {
  scores_text[[i]] <- paste(word, " sentiment: ", scores[word], sep = "")
  i <- i + 1
}

i <- 1
for (word in keywords) {
  scores_weighted_text[[i]] <- paste(word, " sentiment: ", scores_weighted[word], sep = "")
  i <- i + 1
}

lapply(scores_text, write, paste("data/", state, "/ceron/results/results.txt", sep = ""), append=TRUE)
lapply(scores_weighted_text, write, paste("data/", state, "/ceron/results/results-weighted.txt", sep = ""), append=TRUE)
