#!/bin/bash

# Nom du bucket
BUCKET_NAME="bucket_quiberon_video"

# Créer le fichier de configuration JSON
cat <<EOF > lifecycle.json
{
  "rule": [
    {
      "action": {
        "type": "SetStorageClass",
        "storageClass": "ARCHIVE"
      },
      "condition": {
        "age": 3
      }
    },
    {
      "action": {
        "type": "Delete"
      },
      "condition": {
        "age": 6
      }
    }
  ]
}
EOF

# Appliquer la règle de cycle de vie au bucket
gsutil lifecycle set lifecycle.json gs://$BUCKET_NAME

# Supprimer le fichier de configuration JSON
rm lifecycle.json

echo "Règle de cycle de vie appliquée au bucket gs://$BUCKET_NAME"