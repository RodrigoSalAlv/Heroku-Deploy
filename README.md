## Data exploration
We get a year of information about purchases of cellphones, toghether with how many of those purchases has result as a fraud. The information divided in three core databases:
- Collection: which is the general information of the purchases (date, client ID, amount, purchase order, etc.)
- Claim/Fraud: this database gave us the information of purchases that result as a fraud
- Magento: the magento database gave us information regarding the products that where pruchased

We need to cast most of the information due to that many of them was declared as string when we had other types like integers, datetime, floats. Some information needed was inside very long string with not relevant information, so we need to use regular expression to get the information we needed such as: zipcode from the address, sku from the product, carrier, etc. Also some columns need to be splited for easy extraction of information.

We define new columns with the information we needed of each dataset, and at the end we merge the three different data sets in just one table called "Whole_Collection", we will use this database to create the machine learning module and the visualization dashboard
