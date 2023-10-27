# Recommendation-system-social-network

<br/> **It is necessary to implement a recommendation system for posts on a social network, which will return posts for each user at any time that will be shown to the user in his social network feed.**
<br/>
<br/><img align="left" src="https://media.giphy.com/media/atZII8NmbPGw0/giphy.gif" width="400">
> &ensp; **Initial data:**
<br/> &ensp; As basic raw data - table with PostreSQL
<br/>&ensp; 1) **Users** - user data
<br/>&ensp; 2) **Posts** - post data
<br/>&ensp; 3) **Feeds** - user activity data
<br/>&ensp; - *The set of users is fixed and no new ones will appear*
<br/>&ensp; - *Models are not retrained when using services*
<br/>
<br/>

**Uploaded to the repository:**
1. [Download data and EDA.ipynb](https://github.com/ValentinPatrakeev/Recommendation-system-social-network/blob/main/1.%20Download%20data%20and%20EDA.ipynb) - Loading data from the database to the Jupyter Hub, reviewing the data
2. [Create features.ipynb](https://github.com/ValentinPatrakeev/Recommendation-system-social-network/blob/main/2.%20Create%20features.ipynb) - Creation of features and training sample
3. [Train model .ipynb](https://github.com/ValentinPatrakeev/Recommendation-system-social-network/blob/main/3.%20train%20model%20.ipynb) - Training models and assessing their quality on the validation set.
4. [Test service.ipynb](https://github.com/ValentinPatrakeev/Recommendation-system-social-network/blob/main/4.%20test%20service.ipynb) - Imitation of a printer on the jupyter notebook
5. [FastAPI service](https://github.com/ValentinPatrakeev/Recommendation-system-social-network/tree/main/FastAPI) - The service downloads data from PostgreSQL, loads the model and, based on a get request, issues recommendations to each user in JSON format

### Conceptual diagram of working with data
<img src="https://github.com/ValentinPatrakeev/Recommendation-system-social-network/blob/main/FastAPI/schema.png" width="100%">


###  Quality Model Assessment:
- In [train model](https://github.com/ValentinPatrakeev/Recommendation-system-social-network/blob/main/3.%20train%20model%20.ipynb) various metrics and their comparisons are presented.
- The best model based on the metric **HitRate@5** (the metric takes the value = 1 if the user liked 1 or more posts out of 5 posts, 0 if none of the 5 were liked)
-- On test data, the catboost model showed HitRate@5 = 0.866

 
### Start service 
At the moment, the project is not invested in Docker (close to implementation), so you can start the service as follows:
1. **We clone to ourselves locally:**
<br/> <git clone git@github.com:ValentinPatrakeev/Recommendation-system-social-network.git>
2. **create a virtual environment:**
<br/> python -m venv Recommendation-system-social-network
3. **Go to the folder, the virtual environment starts, install the libraries:**
<br/>- cd Recommendation-system-social-network
<br/>- .\\Scripts\\activate
<br/>- pip install -r requirements.txt
4. **start service**
<br/>- cd .\FastAPI
<br/>- uvicorn app:app
5. **You can make the request in the browser or in Postman:**
<br/> ***localhost:8000/post/recommendations/?id=200&time=2023-11-12 22:57:45***
<br/> In this request template you can change the ID and time. Range of possible identifiers: 199 < id < 163206
