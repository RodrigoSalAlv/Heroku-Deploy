# machine-learning-project
### Selected topic
We will analyze a large dataset about purchases that result rejected, with the objective to predict and visualize the patterns that have the clients that get a chargeback or claim, using a machine learning model.

### Reason they selected the topic

Nowadays, the company Magenta gets more chargeback and claims, so for its economy, it's necessary to have more knowledge of what kind of purchase could be. And to make a decision when it shows the alerts. So, we want to predict if a buyer will do a fraudulent purchase. Also, we have enough data to analyze and work with it. 

### Description of the source of data
- **date_created:** The date and hour when the chargeback and claim were created.  
- **date_approved:** The date and hour when the purchase was approved.
- **email:** Consecutive numbers that correspond to a client's email.
- **external_reference:** It's a number that uses Magenta to reference the client's purchase with Mercado Libre.
- **operation_id:** The number that use Mercado Libre to identify a purchase.
- **status:** The status of the buy.
- **status_detail:** The status of the operation, claim or chargeback.
- **transaction_amount:** The total of the purchase.
- **installments:** How many periods it will pay the transaction_amount.
- **payment_type:** The different ways to pay the purchase.
- **billing_address:** The complete address the payment_type require.
- **shipping_address:** The complete address for deliver
- **ship_carrier:** The company which will deliver the purchase.
- **shipping_and_handling:** If the ship_carrier requires an extra amount for delivery.

### Questions we hope to answer with the data

- Is it a safe operation?
- What variables are related to the fraudulent buyer?
- What are the big patterns the purchase shows?
- What range of charges is most likely to be fraudulent?
- What is the fraudulent buyer likely to buy?
- Are fraud operations made from a specific region?

### Provisional machine learning model

* Which model did you choose and why? Supervised Machine Learning will be used for this project, mainly because our data covers operations that we already know that are fraud, this means labeled data. When we dig a little bit more into Supervised Machine learning we know that the classification model will help us in this Fraud detection project.

* How are you training your model? We have one year of operations, fraud operations named as (chargebacks and claims) and approved operations. We'll split data into 75% training set and 25% testing set.

* What is the model's accuracy? 
We ran a logistic regression and RandomOversampler model and we obtained 0.5 of accuracy, there was a lot of data that we had to remove so the model could be ran properly. Definitely there's a lot to improve and consider, maybe some restrictions on the data. We'll have to go deeper as well as run different models so we can determine which one is the best fit for this case.

<img width="459" alt="randomsampler_performance" src="https://user-images.githubusercontent.com/31755703/169733620-a2bf7e2c-a703-4e60-9d44-35a914e2ac16.PNG">


* How does this model work? This is the current performance:

<img width="563" alt="randomsampler_results" src="https://user-images.githubusercontent.com/31755703/169733646-11a03659-ba1a-41c2-9799-45c997b1f392.PNG">

We need to remember that Random Sampler,instances of the minority class are randomly selected and added to the training set until the majority and minority classes are balanced.

## Machine Learning Model Second Segment

### Description of preliminary data preprocessing

After running a Resampling model in the first segment we realized that we had to go one step back. For this part we ran the model again but considering less information. So as part of a data preprocessing we selected specific columns in order to have less noise in the model. 

Remember that the first accuracy score was 0.5 which was the same as a simple guess.
![lessdata](https://user-images.githubusercontent.com/31755703/172079336-1482b42b-382f-40e3-b6a0-18cb65d992e3.PNG)

Considering only the following columns:customer_ID, status, transaction_amount, installments, payment_type, month_created, shp_zipcode, fraud_flag and Item_1 we got an improvement on the balanced_accuracy_score of 0.77

### Description of preliminary feature engineering and preliminary feature selection, including the decision-making process

After the improvement obtained in the last point. We looked for different models that could better answer the questions we are looking for. For this case we decided to go with decision tree and random forest. 

The main reason behind this decision is that the model is best suited as it's name refers to make decisions and determining in this case if a transaction is fraud or not.

In order to use decision tree model and random forest we took even less data into consideration.

![decision_tree_data](https://user-images.githubusercontent.com/31755703/172080055-428640ea-c0d2-423b-935d-f0c31742f70f.PNG)

### Description of how data was split into training and testing sets


Data was splitted considering 75% for training and 25% for testing also taking into account the fact of having stratified splitting due to the number of fraud transactions which is very low compared to the size of the whole database.
![Spliting](https://user-images.githubusercontent.com/31755703/172080350-7b80dc9e-a4b1-4fe4-a78b-2c627ec514a2.PNG)


After running the model these are the results:
![results_decision_tree](https://user-images.githubusercontent.com/31755703/172080519-171fad09-9704-4b29-a8c6-924c567058ed.PNG)

As you may see there was a lot of improvement as for the accuracy score and for the recall.

### Explanation of model choice, including limitations and benefits


Finally we decided to try Random Forest, after all it is an improvement on how decision tree model  works.

The main reasons for this decision are:

#### Random forest algorithms:

* Are robust against overfitting as all of those weak learners are trained on different pieces of the data.
* Can be used to rank the importance of input variables in a natural way.
* Can handle thousands of input variables without variable deletion.
* Are robust to outliers and nonlinear data.
* Run efficiently on large datasets.


#### Interpretation of results:
![image](https://user-images.githubusercontent.com/31755703/172081024-f026a89e-eefb-4fce-8fac-b4a56871a12d.png)

We need to improve the recall score, 0.30 tells us that 30% of the times we'll be right when detecting actual frauds, but 70% of the time we won't. One benefit of the current model is that we are not losing many transactions by classifying them as fraud when they are not, which is good for the business but there's still room for improvement so we can catch all of the fraud transactions. 

We ran the model with 500 n_estimators which are the number of trees that were created by the algorithm. Generally, the higher number makes the predictions stronger and more stable, but can slow down the output because of the higher training time allocated. So for this test we decided to go with 500 and didn't take much time.

Now we can clearly see which features, or columns are more relevant.
![features_random](https://user-images.githubusercontent.com/31755703/172081264-b362a8d4-6353-49c5-b7a5-111bb0068e7b.PNG)
