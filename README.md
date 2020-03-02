# Determining which Sentiment Analysis Predictive Model to use for a given Social Media Election Dataset
Lena Renshaw, 2019-2020, Brown University

## Background and Research
https://docs.google.com/document/d/17qkcn90dSMskabn0-GPWnHcUXmQGfWmI-MtYdr3dM0I/edit#heading=h.lcnpraagn9ul

## Methodology
  https://docs.google.com/document/d/1aUshAt1AmErNO2ZlLKOGE6REbE_bGyHouTWjzzcomb0/edit
  Caucuses and primaries: https://www.270towin.com/2020-election-calendar/

## Detailed Usage Instructions for a Given Election
0. Create filepaths for saving data.
  ```
  python3 general_scripts/create_directories.py <state-name>
  ```

1. Using Python TwitterScraper, scrape data about certain keywords from three weeks before the election to the night before the primary or caucus from the area that the caucus is in.

  Sample query, run from command line:
  ```
  twitterscraper "Bennet OR Biden OR Bloomberg OR Buttigieg OR Gabbard OR Klobuchar OR Patrick OR Sanders OR Steyer OR Warren OR Yang OR Democrat OR dem OR Caucus OR primary near:'<state-name-formatted>' within:10mi" -bd YEAR-MO-DA -ed YEAR-MO-DA -o data/<state-name>/raw_tweets/<state-name>.json
  ```

2. To get results for O'Connor calculations:

  ```
  python3 oconnor/json_to_textfiles.py <state-name>
  cd oconnor/opinionfinderv2.0
  java -Xmx1g -classpath ./lib/weka.jar:./lib/stanford-postagger.jar:opinionfinder.jar opin.main.RunOpinionFinder <state-name>.doclist -d
  cd ../..
  ```
  Move the resulting files from the raw_tweets folder to the oconnor folder.
  ```
  python3 oconnor/calculate_sentiment.py <state-name>
  ```

  The output will be located in `data/<state-name>/oconnor/results`.

3. To get results for Ceron calculations:
  Note: the original methodology for this has people hand-labeling tweets into different sentiments. Right now, I am instead using the O'Connor calculations to do this labeling, because there are too many tweets for me to do so. In the future, we will likely have to implement mechanical turk or something similar to do this labeling and then re-classify the data in order to correctly simulate this.

  To get the training data, do the same query but from the data from four weeks prior to the event to three weeks prior to the event:
  ```
  twitterscraper "Bennet OR Biden OR Bloomberg OR Buttigieg OR Gabbard OR Klobuchar OR Patrick OR Sanders OR Steyer OR Warren OR Yang OR Democrat OR dem OR Caucus OR primary near:'<state-name-formatted>' within:10mi" -bd YEAR-MO-DA -ed YEAR-MO-DA -o data/<state-name>/ceron/<state-name>-ceron-training.json
  python3 ceron/json_to_textfiles.py <state-name>
  cd oconnor/opinionfinderv2.0
  java -Xmx1g -classpath ./lib/weka.jar:./lib/stanford-postagger.jar:opinionfinder.jar opin.main.RunOpinionFinder <state-name>-training-data.doclist -d
  cd ../..
  python3 ceron/get_test_and_train_data.py <state-name>
  ```

  Then, to run the R code, we can do open `ceron/isaX.R`, change the variable `state` to `<state-name>`, and then run:
  ```
  Rscript ceron/isaX.R
  ```

  The output will be located in `data/<state-name>/ceron/results`.

4. To get the Tumasjan calculations:

  Run the following:
  ```
  python3 tumasjan/vader_sentiment.py <state-name>
  python3 tumasjan/process_vader_results.py <state-name>
  ```

  Additionally, run the LIWC software on the `raw_tweets` for the following 12 dimensions: future orientation, past orientation, positive emotions, negative emotions, sadness, anxiety, anger, tentativeness, certainty, work, achievement, and money.

  The output will be located in `data/<state-name>/tumasjan/results`.
