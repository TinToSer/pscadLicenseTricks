## JMS ##
## https://github.com/tintoser
## Developed by TinToSer
import requests
import base64
import warnings
warnings.filterwarnings("ignore")

def getAllLicenses(username,password):  
    session = requests.session()
    url = "https://mycentre.hvdc.ca:443/loginUser.json"
    headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"121\", \"Not A(Brand\";v=\"99\"", "Accept": "application/json, text/plain, */*", "Content-Type": "application/json;charset=UTF-8", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": "https://mycentre.hvdc.ca", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://mycentre.hvdc.ca/login", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9", "Priority": "u=1, i", "Connection": "close"}
    login_json={"password": base64.b64encode(password.encode()).decode(), "username":username }
    _=session.post(url, headers=headers, json=login_json, verify=False)
    url = "https://mycentre.hvdc.ca:443/getAllWorkgroups.json?unique="
    wrkgrps=session.get(url)
    final_data={}
    for each_group in wrkgrps.json()['list']:
        accound_id=each_group['AccountID']
        url = f"https://mycentre.hvdc.ca:443/getWorkgroupInfo.json?workgroupID={accound_id}"
        final_data[each_group['Name']]=session.get(url, verify=False).json()
    return final_data


username=""
password=""
#It will be a dictionary file with keys as GroupId and values as Licenses details
result=getAllLicenses(username,password)
