# RobertVmAPI
Python API created using FASTAPI and Azure CLI , with the end-goal to facilitate the easier provisioning and deprovisioning of vms within Azure.
Written in Python, HTML, Javascript and SQLite.

# How to set this up
### 1) Run this in Git Bash to clone the repository locally
```
git clone https://github.com/RobertTene/RobertAzureAPI
```

### 2) Replace the subscription ID with your azure subscription in "azure_services.py"
```javascript
subscription_id = "ea0ab0bd-6f71-4b45-822b-6626ba8ba20e"  # My current active subscription. Replace this with your subscription ID from Azure.
```

### 3) Install the dependencies via the requirements.txt

```
pip install -r requirements.txt
```

### 4) Authenticate with the user that owns the susbscriptionID in Azure 
```commandline
az login
```
NOTE: This will be improved to use a service principal in the future

### 5) Run the API
```commandline
cd RobertAzureAPI/backend
python main.py
```
### 6)Run the frontend
```commandline
cd RobertAzureAPI/frontend
node app.js
```

### 7) Final step: Demo the web app at http://localhost:3000

Once you access it, it should look like below:

![alt text]([https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png](https://github.com/RobertTene/RobertAzureAPI/blob/main/media/VM%20Project.png)https://github.com/RobertTene/RobertAzureAPI/blob/main/media/VM%20Project.png "Main Page RobertAPI")
