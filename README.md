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
