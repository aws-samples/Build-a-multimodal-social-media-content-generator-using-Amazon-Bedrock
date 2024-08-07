# How to use:

1. Download latest boto3 and botocore python wheel packages by running ``` sh download-dependencies.sh``` in terminal. Update the wheel packages' paths in requirements.txt 
2. In terminal run ``` pip install --no-cache-dir -r requirements.txt ``` to install dependencies. 
3. Update with your own streamilt app logic in ``` app.py ```
4. Install required system packages iproute and jq by running ```sh setup.sh```
5. Run streamlit demo and create shareable link, run this shell script in terminal: ``` sh run.sh ```
6. You can list all running steamlit apps by running this script: ``` sh status.sh ```
7. You can shut down all running streamlit apps by running this script: ``` sh cleanup.sh ```