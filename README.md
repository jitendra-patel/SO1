# so1

Task 1: Create a nagios check that will trigger in case of 3 occurrences of a "Handbill not printed" string
in Elasticsearch. (If you don't know nagios, you could consider creating script that will output
meaningful status)
Solution:-
```
$ python ESClusterErrorCheck.py --host=<ESClusterURL> --port=<ESClusterPort(defaults to 9200)>
```
  
Task 3(most important):
1. Set up (in kubernetes/minikube) 2 pods with a java example app:
https://github.com/TechPrimers/docker-mysql-spring-boot-example 
<br />
Solution:-
<br />
a. Take checkout of this git repo(https://github.com/TechPrimers/docker-mysql-spring-boot-example):-
```
   $ git clone https://github.com/TechPrimers/docker-mysql-spring-boot-example
```
b. Nevigate inside the spring boot application directory:-
```
   $ cd docker-mysql-spring-boot-example
```
b. Create the application jar(users-mysql.jar):-
```
   $ ./mvnw clean package
```
c. Create docker image of spring boot application:-
```
   $ docker build -t docker-mysql-spring-boot-example .
```
d. Authenticate Docker to your default AWS Registry:-
```
   $ aws ecr get-login --region <AWS Region> --no-include-email
   $ docker login -u <AWS Account User Name> -p <AWS Account User Password> https://<AWS Account ID>.dkr.ecr.<AWS Region>.amazonaws.com
```
e. Create a docker repository on AWS ECR:-
```
   $ aws ecr create-repository --repository-name docker-mysql-spring-boot-example --region <AWS Region>
```
f. Tag a docker image to push to your AWS ECR repository(docker-mysql-spring-boot-example):-
```
   $ docker tag docker-mysql-spring-boot-example:docker-mysql-spring-boot-example <AWS Account ID>.dkr.ecr.<AWS Region>.amazonaws.com/docker-mysql-spring-boot-example:docker-mysql-spring-boot-example
```
g. Push the image to AWS ECR:-
```
   $ docker push <AWS Account ID>.dkr.ecr.<AWS Region>.amazonaws.com/docker-mysql-spring-boot-example:docker-mysql-spring-boot-example
```
h. Execute create secret on kubernetes to pull docker image from AWS ECR script before kubernetes deployment:-
```
   $ sh create_secret_pull_image_ecr.sh
```
Start a minikube kubernate cluster:-
```
   $ minikube start
```
b. 
