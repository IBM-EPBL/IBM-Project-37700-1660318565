import requests
import json

API_KEY = "Ba1rsbBXQDZJzM50_I8GR6Qon8VzcFbMxEb_jpiJuEGw"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

payload_scoring = {"input_data": [{"field": [['GRE Score','TOEFL Score','University Rating','SOP','LOR','CGPA','Research']],
                                   "values": [[330,120,4,4,3,8.0,1]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/5225672f-40af-4161-b95f-ac23c62c8581/predictions?version=2022-11-17', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
predictions = response_scoring.json()
pred = predictions['predictions'][0]['values'][0][0]

if(pred == 0):
    print('No Chance of admit')
else:
    print('Chance of admit')