# # Déployez le workflow

project_id=""
workflow_name="my-workflow"
region="europe-west1"




gcloud workflows deploy $workflow_name --source=workflow.yaml --location=$region

