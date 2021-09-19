# **ETL Data covid from API data.covid19.go.id**

![image](https://user-images.githubusercontent.com/55681442/133692288-3e0001e1-98ff-450c-8148-e90d0cd75cbe.png)

This project contain about ETL using airflow, postgree and docker to get data covid19 in indonesia (34 province). The source data from data.covid19.go.id (API public data).But in this project i pass step off installation airflow in docker. if you want to know about installation airflow in docker check this [link](https://youtu.be/J6azvFhndLg).

## 1. Installation Instruction 

a. Copy file DAG_data_covid.py from folder 01.DAG to your DAG folder airflow

b. Make sure your python in airflow already install requirement package (see in file 03.Requirements.txt)

c. Import variabel from folder 02.Airflow variable (in that folder have 2 variable first variable for API component and the second for posgree variable)
![image](https://user-images.githubusercontent.com/55681442/133917842-8b6d1783-bcbb-483e-95bc-f0e80e985132.png)

**Note** : in variable contains server ip postgree please edit to your server ip. if you don't konw ip server postgree please check this [link](https://stackoverflow.com/questions/53610385/docker-postgres-and-pgadmin-4-connection-refused)

d. In folder DAG create folder data and in that folder create folder covid. This folder use for processing transfer variable from postgree to ariflow (using .json file and xcom in airflow)

![image](https://user-images.githubusercontent.com/55681442/133918119-2a41b3b6-ecae-4fe4-843a-a1d79c5aa9b2.png)

## 2. Running and Testing DAG
