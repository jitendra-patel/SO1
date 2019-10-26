# so1

Task 1: Create a nagios check that will trigger in case of 3 occurrences of a "Handbill not printed" string
in Elasticsearch. (If you don't know nagios, you could consider creating script that will output
meaningful status)
Solution:-
```
$ python ESClusterErrorCheck.py --host=<ESClusterURL> --port=<ESClusterPort(defaults to 9200)>
```
  
Task 3(most important):
1. Set up (in kubernetes/minikube) 2 pods with a java example app: https://github.com/TechPrimers/docker-mysql-spring-boot-example  
Solution:-  
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
h. Start a minikube kubernate cluster:-
```
   $ minikube start
```
i. Execute create secret on kubernetes to pull docker image from AWS ECR script before kubernetes deployment:-
```
   $ sh create_secret_pull_image_ecr.sh
```
j. Create the kubernetes secrets to store MYSQL username & its password along with URL:-
```
$ kubectl create secret generic mysql-root-pass --from-literal=password=password
$ kubectl create secret generic mysql-user-pass --from-literal=username=sa --from-literal=password=password
$ kubectl create secret generic mysql-db-url --from-literal=database=polls --from-literal=url='jdbc:mysql://mysql-standalone:3306/test'
```
k. Deploy MySQL by applying the yaml configuration file(mysql-deployment.yaml):-
```
$ kubectl apply -f mysql-deployment.yaml
```
l. Deploy docker-mysql-spring-boot-example application by applying the yaml configuration file(docker-mysql-spring-boot-example.yaml):-
```
$ kubectl apply -f docker-mysql-spring-boot-example.yaml
```

2. Load balance the traffic to the backends.  
Solution:-  
Load balance the traffic of docker-mysql-spring-boot-example application to backend 2 pods by creating its service object as 'LoadBalancer' type:-
```
apiVersion: v1
kind: Service
metadata:                     
  name: docker-mysql-spring-boot-example
  labels:
    app: docker-mysql-spring-boot-example
spec:                         
  type: LoadBalancer 
  selector:
    app: docker-mysql-spring-boot-example   # The service exposes Pods with label `app=polling-app-server`
  ports:                      # Forward incoming connections on port 80 to the target port 8080
  - name: http
    port: 80
    targetPort: 8080
```

3. Create policy to auto-heal or recreate the pod if it goes down or is unresponsive.  
Solution:-  
```
$ kubectl scale deployment docker-mysql-spring-boot-example --replicas=2
```

4. Add a mysql.  
Solution:-  
```
$ kubectl apply -f mysql-deployment.yaml
```

5. Can you do a HA of a database? Any way to keep the data persistent when pods are recreated?    
Solution:-  
HA of a MYSQL database can be maintained by having below configuration in mysql-deployment.yaml, which ensure the running of one MYSQL POD always and spin up the new MYSQL POD as soon as old POD stops working:-
```
strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
    type: RollingUpdate
  replicas: 1
```
Data persistency can be maintained even after recreation of MYSQL POD by having below configuration in its YAML file:-
```
apiVersion: v1
kind: PersistentVolume            # Create a PersistentVolume
metadata:
  name: mysql-pv
  labels:
    type: local
spec:
  storageClassName: standard      # Storage class. A PV Claim requesting the same storageClass can be bound to this volume. 
  capacity:
    storage: 250Mi
  accessModes:
    - ReadWriteOnce
  hostPath:                       # hostPath PersistentVolume is used for development and testing. It uses a file/directory on the Node to emulate network-attached storage
    path: "/mnt/data"
  persistentVolumeReclaimPolicy: Retain  # Retain the PersistentVolume even after PersistentVolumeClaim is deleted. The volume is considered “released”. But it is not yet available for another claim because the previous claimant’s data remains on the volume. 
---    
apiVersion: v1
kind: PersistentVolumeClaim        # Create a PersistentVolumeClaim to request a PersistentVolume storage
metadata:
  name: mysql-pv-claim
  labels:
    app: polling-app
spec:
  storageClassName: standard       # Request a certain storage class
  accessModes:
    - ReadWriteOnce                # ReadWriteOnce means the volume can be mounted as read-write by a single Node
  resources:
    requests:
      storage: 250Mi
---
```
6. Add CI to the deployment process.  
Solution:-  
Push the jenkinsfiles(checked in this repo for your ref) along with application code base in each git branch(dev/qa/prod) so that CI/CD will be get trigger upon every successful commit to Git repo after setup of jenkins job on Jenkins console.  

7. Split your deployment into prd/qa/dev environment.  
Solution:-  
Deployment on dev/qa/prod will be performed based on mentioned configuration in jenkinsfiles and commits made in git branch(dev/qa/prod) respectively. Please refer committed jenkinsfiles for exact implementation of deployment on dev/qa/prod.  

8. Please suggest a monitoring solution for your system. How would you notify an admin
that the resources are scarce?  
Solutions:-  
