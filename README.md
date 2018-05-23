# Turkish Sentiment Analysis for Twitter

## **Required libraries / packages:**  <br>
  • Python 3  <br>
  • Numpy for Python 3  <br>
  • scikit-learn for Python 3 <br>

Train documents in [src/Train directory](https://github.com/hilalbenzer/BOUNSentimentAnalysis/tree/master/src/Train).

Test documents in test_tweets

## **Usage**
1. Pull the repository
2. ``` $ cd BOUNSentimentAnalysis/src ```
3. To train ``` $ python3 Train_data.py ```
4. To test using Bag of Words:  <br>
  • Multinomial Naive Bayes: ``` $ python3 Test_data_MNB.py  ``` <br> 
  • Support Vector Machine:   ```    $ python3 Test_data_SVM.py    ``` <br>
  • K-Nearest Neighbors: ``` $ python3 Test_data_KNN.py <neighbor_count> ```  <br>
5. To test using 2-grams: <br>
  • Multinomial Naive Bayes:  ``` $ python3 Test_data_MNB.py bigram ``` <br>
  • Support Vector Machine: ``` $ python3 Test_data_SVM.py bigram ``` <br>
  • K-Nearest Neighbors: ``` $ python3 Test_data_KNN.py <neighbor_count> bigram ``` <br>
