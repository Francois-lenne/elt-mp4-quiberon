# you need to run this command in the directory of the integrations programs in the src

gcloud functions deploy "retrieve_quiberon_video" --runtime python39 --trigger-http --allow-unauthenticated --entry-point=main --timeout=3600s