# Kaggle Users Tutorial 

This repository represents scraping user data found on page.

## Case
- Get list of username(s), create link(s), f.e. `https://www.kaggle.com/lsind18`
- Check presence of user page
- Parse user data, including username, userid, bio, last access date and all statistics about user datasets, notebooks, competitions, discussions
- Transform data in relational format
- Insert tranformed data into database
- If data about this user was already parsed within last 12 hours, log it and parse next user

#
## Independent webscraping
### Prerequisites
- **>=Python3.10**
- install requirements (requests, bs4, sqlalchemy)
```cmd
pip install -r requirements.txt
```

### Project Structure
```
 ..independent_parsing  
    ├── project_setup  
    |   ├── logs/                   # Logs will appear here
    |   ├── context_setup.py        # DB connection, SQL tables, mapping to Model  
    │   └── logger_setup.py         # Logger setup  
    |   
    ├── process_data                      
    │   ├── Model.py                # Classes Users, UserStats, Stats  
    │   ├── Repository.py           # Insert Model objects into database   
    │   └── Service.py              # Tranform parsed data (dict), create Model objects  
    |
    ├── main.py                     # Get usernames, read data from pages --> dict  
    ├── requirements.txt  
    ├── kaggle_users.db             # Database for local testing 
    └── usernames.txt               # File with list of usernames
```

### Database Structure
 - database structure with ORM SqlAlchemy (context_setup.py): create db or use existing
 - classes Users, UserStats, Stats (Model.py)

![ER diagram](https://www.dropbox.com/s/wubpd4u3p4h9lrv/db-kaggle-users.JPG?raw=1)

### Sample data 
Data which was already parsed, tranformed and inserted into dataabse.
- Table Users

| id      | userId             | userName            | userJoinDate                   |
|---------|--------------------|---------------------|--------------------------------|
| 1       | 2913628            | lsind18             | 2019-03-08 18:01:26.933000     |
| ..      | .......            | ........            | ........                       |

- Table UserStats

| statsid | userId | displayName     | country    | city             | region   | bio              | userLastActive            | performanceTier | followers | following | parsedate|
|---------|--------|-----------------|------------|------------------|----------|------------------|---------------------------|-----------------|------------|----------|----------|
| 1       | 1      | Daria Chemkaeva | Russia     | Saint Petersburg |          | Чемкаева Дарья...|2023-05-31 17:25:00.747000 | EXPERT          | 53         | 19        | 2023-06-01 12:16:08.339119 |
| ..      | .....  |                 | ........   | ........         |          |                  |                           |                 |            |                  |        

- Table Stats

| id | userstatsId | statsType           | tier        | totalResults | rankPercentage | rankOutOf | rankCurrent | rankHighest | totalGoldMedals | totalSilverMedals | totalBronzeMedals |
|----|-------------|---------------------|-------------|--------------|----------------|-----------|-------------|-------------|-----------------|-------------------|-------------------|
| 1  | 1           | competitionsSummary | CONTRIBUTOR | 2            | 0.9209785      | 3742      |             |             |                 |                   |                   |
| 2  | 1           | scriptsSummary      | EXPERT      | 9            | 0.014632434    | 279106    | 4084        | 773         |                 | 1                 | 6                 |
| 3  | 1           | datasetsSummary     | EXPERT      | 16           | 0.009669507    | 91318     | 883         | 95          |                 | 1                 | 10                |
| 4  | 1           | discussionsSummary  | EXPERT      | 83           | 0.008640102    | 345945    | 2989        | 2125        |                 |                   | 50                |
| 5  | 2           | ..                  | ..          | ..           |                |           |             |             |                 |                   |                   |

### Project Logic
![Project Graph](https://www.dropbox.com/s/axkbvkz3macwh9l/workflow.JPG?raw=1)

### Use 
- put usernames you are interested in into file usernames.txt
- start main.py (entry point)
- user statistics data will only be inserted into database if it have passed more than 12 hours since last parse
- all data goes to sqlite database. You can change connection or use another RDBMS in `project_setup/context_setup.py`. Don't forget to install database provider
- datetime columns are in UTC
- log files created in `project_setup/logs` folder
- give these scripts to any scheduler (cron, Task Scheduler, etc)

#
## Use apache-airflow
**PROJECT ON UPDATE**

### Prerequisites

- **>=Python3.10**
- virtual environment
```cmd
python3 -m venv virt_env
source virt_env/bin/activate
```
- install requirements
```cmd
pip install -r requirements.txt
```
- set up airflow
```cmd
export AIRFLOW_HOME="path to current directory"
airflow db init
airflow users create
    --username
    --firstname
    --lastname
    --role Admin
    --email
```
- if airflow database was not created properly, recreate it
```cmd
airflow db reset
```
- check dag
```cmd
airflow dags list
```

- run webserver, run scheduler
```cmd
airflow scheduler
airflow webserver
```
- log into webserver local url with created user

### Project Structure

```
 ..airflow_parsing  
    ├── dags  
    |   ├── 
    │   └── 
    |   
    ├── process_data                      
    │   ├── 
    │   ├── 
    │   └──   
    |
    ├── logs/                       # Logs will appear here  
    |
    ├── airflow.cfg                 # Config airflow, dags folder, database, etc  
    ├── webserver_config.cfg        # Webserver config if necessary 
    ├── airflow.db                  # Airflow Db created  
    ├── requirements.txt  
    ├──                             # Database for local testing 
    └── usernames.txt               # File with list of usernames
```

### Dag Structure
