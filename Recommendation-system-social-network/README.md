# Recommender System
This repository presents an integrated approach to creating a recommendation system service.

* Uploaded to the repository:
1. [Download data and EDA.ipynb](https://github.com/ValentinPatrakeev/Recommendation-system-social-network/blob/main/Recommendation-system-social-network/1.%20Download%20data%20and%20EDA.ipynb) - Loading data from the database to the Jupyter Hub, reviewing the data
2. [Create features.ipynb](https://github.com/ValentinPatrakeev/Recommendation-system-social-network/blob/main/Recommendation-system-social-network/2.%20Create%20features.ipynb) - Creation of features and training sample
3. [Train model .ipynb](https://github.com/ValentinPatrakeev/Recommendation-system-social-network/blob/main/Recommendation-system-social-network/3.train%20model%20.ipynb) - Training models and assessing their quality on the validation set.
4. [Test service.ipynb](https://github.com/ValentinPatrakeev/Recommendation-system-social-network/blob/main/Recommendation-system-social-network/4.%20test%20service.ipynb) - Imitation of a printer on the jupyter notebook
5. [FastAPI service](https://github.com/ValentinPatrakeev/Recommendation-system-social-network/tree/main/Recommendation-system-social-network/FastAPI) - The service downloads data from PostgreSQL, loads the model and, based on a get request, issues recommendations to each user in JSON format

### Conceptual diagram of working with data, training and creating services is presented in the diagram

<img src="https://github.com/ValentinPatrakeev/Recommendation-system-social-network/blob/main/Recommendation-system-social-network/FastAPI/schema.png" width="100%">


1. Loading data from the database to the Jupyter Hub, reviewing the data:
file - 1. Download data and EDA.ipynb
	
	-General Data View with matplotlim pyplot.
	-We have 3 table (users, posts, feed)
		users - size 163205
		posts - size 7023
		feeds - size to more 80 million (cut to 5 million)
	-Save date to format scv for comfortable local work
	-aggregation data with help SQL query ('post popularity')
			

2. Creation of features and training sample. For example, user attributes, message texts, and other statistical data may be used.
file -  Create features.ipynb	
	
	-Create features by users (all users 163205) - download on PostgreSQL
	-Create features by posts  - download on PostgreSQL
	-Create databse train_data (by users who fell into the сut sample) - save on local laptope 

3. Training models on Jupyter Hub and assessing their quality on the validation set.
file -  3.train model .ipynb
	
	-preparation date for model (separate numeric and categorical columns, sorted for time, drop not need columns, separation on the train and the test validation)
	-Use CatBoostClassifier
	-save model

4.  Imitation of a printer on the jupyter notebook
file -  4. test service.ipynb	

	loading a model -> 
	getting results for models by user_id -> 
	predicting posts that will be liked -> 
	returning a response.


5. Writing a service FastAPI with pycahrm:
	
