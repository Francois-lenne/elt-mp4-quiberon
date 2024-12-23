# Variables
project_id=""
repo="quiberon"
region="europe-west1"
description="Depot de conteneurs pour le projet quiberon"

# Créez le dépôt Artifact Registry
gcloud artifacts repositories create $repo --repository-format=docker --location=$region --description="$description"

# Construisez l'image Docker
docker build -t $region-docker.pkg.dev/$project_id/$repo/transformation:latest .


# Poussez l'image Docker vers Artifact Registry
docker push $region-docker.pkg.dev/$project_id/$repo/transformation:latest

# Créez un job Cloud Run
gcloud beta run jobs create transformation-job \
    --image=$region-docker.pkg.dev/$project_id/$repo/transformation:latest \
    --region=$region

# Exécutez le job Cloud Run
gcloud beta run jobs execute transformation-job --region=$region