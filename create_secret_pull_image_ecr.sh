ACCOUNT=<AWS Account ID>
REGION=<AWS Region>
SECRET_NAME=${REGION}-ecr-registry

# Fetch token which get expire in every 12 hours
TOKEN=`aws ecr --region=$REGION get-authorization-token --output text --query authorizationData[].authorizationToken | base64 -d | cut -d: -f2`

# Create or replace registry secret
kubectl delete secret --ignore-not-found $SECRET_NAME
kubectl create secret docker-registry $SECRET_NAME \
 --docker-server=https://${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com \
 --docker-username=<AWS Account User Name> \
 --docker-password="${TOKEN}"
