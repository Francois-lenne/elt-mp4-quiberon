workflow_name=""
project_id=""
scheduler_name=""
region=""


gcloud scheduler jobs create $scheduler_name \
  --schedule "0 8 * * *" \
  --time-zone "Europe/Paris" \
  --uri "https://workflowexecutions.googleapis.com/v1/projects/$project_id/locations/$region/workflows/$workflow_name/executions" \
  --http-method POST