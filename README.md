# Description of the projects


This project involves developing an ETL (Extract, Transform, Load) pipeline capable of processing unstructured video from the beacg municipal camera of the town of Quiberon.

The aim is to extract the videos, use the OpenCV2 library to analyze and process the video data in order to see if there is at least one person in the beach, then save the results in a BigQuery database for further analysis.




# Architecture of the project 


## stack 

<p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img src="https://go-skill-icons.vercel.app/api/icons?i=py,docker,git,gcp,github,githubactions,bigquery" />
  </a>
</p>


## Architecture 


![quiberon (1)](https://github.com/user-attachments/assets/6aa5d5e0-e9b0-4083-a666-8de7602418f8)


## Spec 

### Cloud functions


* memory 512 mio
  
* timeout 600 seconds

### Google cloud run

* memory 4gio

* timeout 1200 seconds


## file management 

### root 

in the root folder you can found the cloudbuild.yml file in order to do the CI/CD for the google cloud function and google cloud run and the ignore file and the requirements.txt for all the ELT 


### src


in the src folder you have two folders one is for data transformation (treatments of the video) and the other data_integrations in order to retrieve all the video from the last day




### config 


in the config folder you can find all the script bash in order to depoy this projects 



# Contact/ Questions 


Don't hesitate to ask me questions about this project ! 


Reach me by email (in my github profile) or with an issue in this repo
