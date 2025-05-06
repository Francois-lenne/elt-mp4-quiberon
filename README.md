# Quiberon Beach Video Analytics

## 📝 Project Description

This project implements an ETL (Extract, Transform, Load) pipeline that processes video footage from the municipal beach camera in Quiberon. The system extracts videos, uses OpenCV with YOLO object detection to identify if people are present on the beach, and stores analysis results in BigQuery for further analysis and visualization.

<p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img src="https://go-skill-icons.vercel.app/api/icons?i=py,docker,git,gcp,github,githubactions,bigquery" />
  </a>
</p>

## 🏗️ Architecture

![Quiberon Project Architecture](https://github.com/user-attachments/assets/6aa5d5e0-e9b0-4083-a666-8de7602418f8)

### Components

1. **Cloud Function** - Retrieves video footage from the municipal camera feed
2. **Cloud Storage** - Stores the video files temporarily
3. **Cloud Run** - Processes videos using YOLO object detection
4. **BigQuery** - Stores analysis results for querying
5. **Workflows** - Orchestrates the entire pipeline
6. **Cloud Scheduler** - Triggers the workflow daily

### Technical Specifications

#### Cloud Functions
- Memory: 512 MB
- Timeout: 600 seconds

#### Google Cloud Run
- Memory: 4 GB
- Timeout: 1200 seconds

## 🚀 Setup & Installation

### Prerequisites

- Google Cloud Platform account with billing enabled
- `gcloud` CLI installed and configured
- Docker installed (for local testing)
- Python 3.9 or higher

### Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/quiberon-beach-analytics.git
   cd quiberon-beach-analytics
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download YOLO model files:
   ```bash
   bash config/dowload_file_for_yolo.sh
   ```

### GCP Resource Setup

1. Create a GCP project and note your Project ID

2. Enable required APIs:
   ```bash
   gcloud services enable \
     cloudfunctions.googleapis.com \
     run.googleapis.com \
     artifactregistry.googleapis.com \
     cloudbuild.googleapis.com \
     workflows.googleapis.com \
     cloudscheduler.googleapis.com \
     bigquery.googleapis.com
   ```

3. Create the BigQuery dataset and table:
   ```bash
   bq mk --dataset --location=EU your-project-id:video_quiberon
   bq query --use_legacy_sql=false < src/sql_script/DDL_bigquery.sql
   ```

4. Create a Cloud Storage bucket:
   ```bash
   gsutil mb -l europe-west1 gs://bucket_quiberon_video
   ```

5. Apply lifecycle rules to the bucket:
   ```bash
   bash config/lifecycle_rule.sh
   ```

## 🔄 Deployment

### Manual Deployment

1. Deploy Cloud Function:
   ```bash
   cd src/data_integration
   gcloud functions deploy retrieve_quiberon_video \
     --runtime python39 \
     --trigger-http \
     --allow-unauthenticated \
     --entry-point=main \
     --timeout=3600s
   ```

2. Deploy Cloud Run job:
   ```bash
   # First, update project_id in config/deploy_container.sh
   bash config/deploy_container.sh
   ```

3. Deploy Workflow:
   ```bash
   # First, update project_id in config/workflow.sh
   bash config/workflow.sh
   ```

4. Create Scheduler:
   ```bash
   # First, update variables in config/scheduler.sh
   bash config/scheduler.sh
   ```

### CI/CD Deployment

Alternatively, use the included Cloud Build configuration:

1. Update the substitution variables in `cloudbuild.yaml` if needed

2. Trigger the CI/CD pipeline:
   ```bash
   gcloud builds submit
   ```

## 📁 Project Structure

```
.
├── .cloudignore          # Files to ignore in cloud deployments
├── .gitignore            # Files to ignore in git
├── README.md             # This documentation
├── cloudbuild.yaml       # CI/CD configuration
├── config/               # Deployment scripts
│   ├── deploy_container.sh
│   ├── dowload_file_for_yolo.sh
│   ├── lifecycle_rule.sh
│   ├── scheduler.sh
│   ├── setup_cloud_function.sh
│   ├── workflow.yml
│   └── workflow.sh
└── src/                  # Source code
    ├── data_integration/ # Video retrieval component
    │   ├── main.py
    │   └── requirements.txt
    ├── data_transformation/ # Video analysis component
    │   ├── dockerfile
    │   ├── dowload_file_for_yolo.sh
    │   ├── model.py
    │   ├── transform.py
    │   └── requirements.txt
    └── sql_script/       # Database scripts
        └── DDL_bigquery.sql
```

## 🔍 How It Works

1. **Data Extraction**: The Cloud Function (`retrieve_quiberon_video`) retrieves video footage from the previous day from the Quiberon beach camera and stores it in Cloud Storage.

2. **Data Transformation**: A Cloud Run job (`transformation-job`) processes the videos using YOLO object detection to identify frames containing people.

3. **Data Loading**: Analysis results are loaded into BigQuery for querying and visualization.

4. **Orchestration**: A Cloud Workflow orchestrates the entire process, first triggering the Cloud Function, then the Cloud Run job.

5. **Scheduling**: A Cloud Scheduler job triggers the workflow daily at 8:00 AM (Paris time).

## 🔧 Customization

### Changing the Video Source

To analyze videos from a different source, modify the URL pattern in `src/data_integration/main.py`:

```python
url = f"https://your-new-video-source.com/path/{date_formatee}/{hour_str}-{minute_str}.mp4"
```

### Adjusting the Analysis Parameters

To change the object detection parameters, modify the confidence threshold in `src/data_transformation/model.py`:

```python
if confidence > 0.5 and self.classes[class_id] == "person":
```

## 📊 Accessing Results

Query the BigQuery dataset to analyze results:

```sql
SELECT 
  day, 
  hour, 
  COUNT(*) as total_frames,
  SUM(CASE WHEN person_present THEN 1 ELSE 0 END) as frames_with_people,
  ROUND(SUM(CASE WHEN person_present THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as percentage_with_people
FROM 
  `your-project-id.video_quiberon.named_result_ml_bronze`
GROUP BY 
  day, hour
ORDER BY 
  day DESC, hour ASC;
```

## 🐛 Troubleshooting

### Common Issues

#### Cloud Function Timeouts
- Increase the timeout value in `config/setup_cloud_function.sh`
- Split the workload into smaller chunks

#### Missing YOLO Model Files
- Make sure to run the `dowload_file_for_yolo.sh` script
- Check that the files are in the correct location

#### Permission Denied Errors
- Make sure your service account has the necessary IAM roles:
  - Cloud Functions Admin
  - Cloud Run Admin
  - Storage Admin
  - BigQuery Data Editor

## 📞 Contact & Questions

Don't hesitate to ask questions about this project!

Reach me by email (in my GitHub profile) or create an issue in the repository.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
