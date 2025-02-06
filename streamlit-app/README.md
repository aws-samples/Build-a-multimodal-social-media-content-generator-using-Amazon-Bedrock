# How to run the Demo :

1. In terminal run ``` pip install --no-cache-dir -r requirements.txt ``` to install dependencies.
2. Run streamlit  ``` streamlit run app.py ```. You will see an output like this:
   ```
   Collecting usage statistics. To deactivate, set browser.gatherUsageStats to False.

   You can now view your Streamlit app in your browser.
    
   Network URL: http://169.255.255.2:8501
   ```
3. Open a new browser tab, copy the address of your current tab and change the address of the tab (i.e. `/proxy/8501/`) as follows.
   Use the same port i.e. `8501` as shown in the output of step 2:
   
   ``` https://XXXXXX.studio.us-east-1.sagemaker.aws/jupyterlab/default/proxy/8501/ ```
   
5. You can shut down all running streamlit apps by running this script: ``` sh cleanup.sh ```

# Updating the demo

1. Update with your own streamilt app logic in ``` app.py ```
