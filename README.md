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

In the following figure we show the relation of the dataset:

![Data_structure](Data_structure.png)


### Questions we hope to answer with the data

- Is it a safe operation?
- What variables are related to the fraudulent buyer?
- What are the big patterns the purchase shows?
- What range of charges is most likely to be fraudulent?
- What is the fraudulent buyer likely to buy?
- Are fraud operations made from a specific region?

## Data exploration
We get a year of information about purchases of cellphones, together with how many of those purchases has result as a fraud. The information was divided in three core databases:
- Collection: which is the general information of the purchases (date, client ID, amount, purchase order, etc.)
- Claim/Fraud: this database gave us the information of purchases that result as a fraud or have a claim by the customer.
- Magento: the magento database gave us information regarding the products that where pruchased in each pruchase order

We needed to cast most of the information due to that many of them was declared as string when the databases had other types like integers, datetime, floats. Some information needed was inside of a very long string with not relevant information, so we need to use regular expression to get the information we needed such as: zipcode from the address, sku from the product, carrier, etc. Also some columns need to be splited for easy extraction of information. To get the information needed we use regular expressions.

![image](https://user-images.githubusercontent.com/96214489/172073457-989535c2-0183-42d4-bd29-3e3c3ff06bb1.png)


We define new columns with the information we needed of each dataset, and at the end we merge the three different data sets in just one table called "Whole_Collection", we will use this database to create the machine learning module.

![image](https://user-images.githubusercontent.com/96214489/172073469-93fb528a-9e6e-48e2-9762-b7a3b60aa6ff.png)

We needed to merge the "Whole_Collection" table with a table of postal codes that we obtained via SEPOMEX; we called this second table as "CPs_Geometry".
Once we get both tables, these two were uploaded to AWS to have them availables for the machine learning project.

The merge will be used for the visualization: this will give us visibility regarding where the pruchases were made and found a tendency to corroborate with the machine learning model. The merge will been performed via colab and with the help of pyspark.sql funcitons

![image](https://user-images.githubusercontent.com/96214489/172073671-92048dfc-6127-4779-b5f3-ed732281bc25.png)

The last table obtained by this merge will be called "whole_collection_geom" and this will be storage in a AWS database and in a bucket to be available for the visibility, as well as in postgres for any analysis needed.

![image](https://user-images.githubusercontent.com/96214489/172073862-9db3b9d1-8e77-4479-98b1-656d773519ee.png)

### Provisional machine learning model

* Which model did you choose and why? Supervised Machine Learning will be used for this project, mainly because our data covers operations that we already know that are fraud, this means labeled data. When we dig a little bit more into Supervised Machine learning we know that the classification model will help us in this Fraud detection project.

* How are you training your model? We have one year of operations, fraud operations named as (chargebacks and claims) and approved operations. We'll split data into 75% training set and 25% testing set.

* What is the model's accuracy? 
We ran a logistic regression and RandomOversampler model and we obtained 0.5 of accuracy, there was a lot of data that we had to remove so the model could be ran properly. Definitely there's a lot to improve and consider, maybe some restrictions on the data. We'll have to go deeper as well as run different models so we can determine which one is the best fit for this case.

<img width="459" alt="randomsampler_performance" src="https://user-images.githubusercontent.com/31755703/169733620-a2bf7e2c-a703-4e60-9d44-35a914e2ac16.PNG">


* How does this model work? This is the current performance:

<img width="563" alt="randomsampler_results" src="https://user-images.githubusercontent.com/31755703/169733646-11a03659-ba1a-41c2-9799-45c997b1f392.PNG">

We need to remember that Random Sampler,instances of the minority class are randomly selected and added to the training set until the majority and minority classes are balanced.



