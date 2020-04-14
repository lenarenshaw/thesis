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
state <- 'illinois'

keywords <- list('biden', 'gabbard','sanders')
scores <- list()
scores_weighted <- list()
scores_add_sub <- list()

scores_text <- list()
scores_weighted_text <- list()
scores_add_sub_text <- list()

min_val = Inf

processFile = function(filepath) {
  lines_as_vector = c()
  con = file(filepath, "r")
  while ( TRUE ) {
    line = readLines(con, n = 1)
    if ( length(line) == 0 ) {
      return(lines_as_vector)
    }
    lines_as_vector = append(lines_as_vector, line)
  }
  close(con)
}

for (word in keywords) {
  # train <- read.csv(file = paste('data/', state, '/ceron/all-training-data.csv', sep=""), header=T)
  train <- read.csv(file = paste('data/ceron/training.csv', sep=""), header=T)
  # test <- read.delim(file = paste('data/', state, '/raw_tweets/', word, '.txt', sep = ""), header = F, sep = "\n")

  # train_data<-stem_words(train[["Word"]])
  # train_labels<-stem_words(train[["Polarity"]])
  # test_data <- stem_words(test[["Word"]])
  train_data <- train[["tweet"]]
  train_labels <- train[["sentiment"]]
  test_data <- processFile(paste('data/', state, '/raw_tweets/', word, '.txt', sep = ""))

  if (length(train_data) > 0 && length(test_data) > 0) {
    num <- 0
    denom <- 0
    total <- 0

    train_data_vector = c()
    train_labels_vector = c()
    test_data_vector = c()

    for (i in c(0:length(train_data))) {
      if (!strcmp(toString(train_data[i]), "") && !strcmp(toString(train_labels[i]), "")) {
        train_data_vector = append(train_data_vector, train_data[i])
        train_labels_vector = append(train_labels_vector, train_labels[i])
      }
    }

    for (i in c(0:length(test_data))) {
      if (!strcmp(test_data[i], "")) {
        test_data_vector = append(test_data_vector, test_data[i])
      }
    }

    results <- iSA(train_data_vector, test_data_vector, train_labels_vector, predict=T)
    preds <- results[6][["pred"]]
    for (sentiment in preds) {
      total <- total + 1
      if (strcmp(sentiment, "2")) {
        denom <- denom + 1
      } else if (strcmp(sentiment, "5")) {
        denom <- denom + 2
      } else if (strcmp(sentiment, "4")) {
        num <- num + 1
      } else if (strcmp(sentiment, "6")) {
        num <- num + 2
      }
    }
    scores[[word]] <- num/(num + denom)
    scores_weighted[[word]] <- num/(num + denom)*total
    scores_add_sub[[word]] <- num - denom
    if ((num - denom) < min_val) {
      min_val = num - denom
    }
  } else {
    scores[[word]] <- 0
    scores_weighted[[word]] <- 0
    scores_add_sub[[word]] <- num - denom
  }
}

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

i <- 1
min_val = abs(min_val)
for (word in keywords) {
  print(as.numeric(scores_add_sub[word]) + as.numeric(min_val))
  scores_add_sub_text[[i]] <- paste(word, " sentiment: ", as.numeric(scores_add_sub[word]) + as.numeric(min_val), sep = "")
  i <- i + 1
}

#lapply(scores_text, write, paste("data/", state, "/ceron/results/results.txt", sep = ""), append=TRUE)
#lapply(scores_weighted_text, write, paste("data/", state, "/ceron/results/results-weighted.txt", sep = ""), append=TRUE)
lapply(scores_add_sub_text, write, paste("data/", state, "/ceron/results/results-modified.txt", sep = ""), append=TRUE)
