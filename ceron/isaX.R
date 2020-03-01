# install.packages("devtools")
# library(devtools)
# install.packages(c("tm", "BMS", "quadprog", "rJava", "parallel", "data.table", "entropy"))
# install_github("blogsvoices/iSAX")
# library(iSAX)
# library(textstem)
# library(pracma)
# setwd("thesis")
# usage: iSA(train_data, test_data, train_labels, predict=TRUE)


x <- read.csv(file = 'data/newhampshire/ceron/bennet_training_data.csv', header=T)
y <- read.csv(file = 'data/newhampshire/ceron/biden_training_data.csv', header=T)
train_data<-c(stem_words(x$Word))
train_labels<-c(stem_words(x$Polarity))
test_data <- c(stem_words(y$Polarity))

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

fileConn<-file("data/newhampshire/ceron/results.txt")
writeLines(c(paste("biden sentiment: ", num/denom)), fileConn)
close(fileConn)

fileConn<-file("data/newhampshire/ceron/results-weighted.txt")
writeLines(c(paste("biden sentiment: ", num/denom*total)), fileConn)
close(fileConn)

