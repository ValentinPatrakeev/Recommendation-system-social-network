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

### Main libraries used
![PANDAS](https://img.shields.io/badge/PANDAS-1.4.2-090909??style=flat-square&logo=PANDAS)
![NUMPY](https://img.shields.io/badge/NUMPY-1.22.4-090909??style=flat-square&logo=NUMPY)
![fastapi](https://img.shields.io/badge/FASTAPI-0.75.1-090909??style=flat-square&logo=fastapi)
![sqlalchemy](https://img.shields.io/badge/SQLALCHEMY-1.4.35-090909??style=flat-square&logo=sqlalchemy)
![catboost](https://img.shields.io/badge/CATBOOST-1.0.6-090909??style=flat-square&logo=catboost)
![pydantic](https://img.shields.io/badge/PYDANTIC-1.9.1-090909??style=flat-square&logo=pydantic)
![psycopg2](https://img.shields.io/badge/PSYCOPG2-2.9.3-090909??style=flat-square&logo=psycopg2)
![uvicorn](https://img.shields.io/badge/UVICORN-0.16.0-090909??style=flat-square&logo=uvicorn)

###  Quality Model Assessment:
- In [train model](https://github.com/ValentinPatrakeev/Recommendation-system-social-network/blob/main/3.%20train%20model%20.ipynb) various metrics and their comparisons are presented.
- The best model based on the metric **HitRate@5** (the metric takes the value = 1 if the user liked 1 or more posts out of 5 posts, 0 if none of the 5 were liked)
-- On test data, the catboost model showed HitRate@5 = 0.866

 
### Start service 
### Start service 
At the moment, the project is not invested in Docker (close to implementation), so you can start the service as follows:

1. **Clone the project locally:**
   <br/> `git clone git@github.com:ValentinPatrakeev/Recommendation-system-social-network.git`

2. **Navigate to the project folder:**
   <br/> `cd Recommendation-system-social-network`

3. **Install dependencies using Poetry:**
   <br/> `poetry install`

4. **Request the `.env` file** – this file should contain the PostgreSQL service key.

5. **Start the service:**
   <br/>- **Activate the virtual environment:**
     <br/> `poetry shell`
   <br/>- **Run the FastAPI server:**
     <br/> `poetry run uvicorn app:app --host 0.0.0.0 --port 8000`

6. **Test the service using a browser or Postman:**
   <br/> `http://localhost:8000/post/recommendations/?id=200&time=2023-11-12%2022:57:45`
   <br/> In this request template, you can change the ID and time. Range of possible IDs: `199 < id < 163206`.
