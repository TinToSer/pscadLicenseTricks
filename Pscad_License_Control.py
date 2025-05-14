## JMS ##
## https://github.com/tintoser
## Developed by TinToSer
## Love to GPT-4

import requests
from bs4 import BeautifulSoup

def get_pscad_license_usage(username, password):
    session = requests.session()
    headers = {
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua": "\"Chromium\";v=\"135\", \"Not-A.Brand\";v=\"8\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://mycentre.pscad.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i"
    }
    lic_db = {}
    url = "https://mycentre.pscad.com:443/logics/ajax/login/ajx-login-submission.php"
    files = {
        "postUsername": (None, username),
        "postPassword": (None, password)
    }
    response = session.post(url, headers=headers, files=files)
    if response.ok:
        url = "https://mycentre.pscad.com:443/logics/ajax/workgroup/ajx-wrkCard-view.php"
        response = session.get(url)
        json_data = response.json()
        html_data = json_data.get("layout")
        soup = BeautifulSoup(html_data, 'html.parser')
        workgroups = soup.find_all('div', class_='cardLineItem')
        for wg in workgroups:
            name = wg.find('div', class_='columnWorkgroupsName').text.strip()
            creation = wg.find('div', class_='columnWorkgroupsCreation').text.strip()
            expiration = wg.find('div', class_='columnWorkgroupsExpiration').text.strip()
            maintenance = wg.find('div', class_='columnWorkgroupsMaintenanceExpiry').text.strip()
            members = wg.find('div', class_='columnWorkgroupsMembers').text.strip()
            licenses = wg.find('div', class_='columnWorkgroupsLicenses').text.strip()
            join_codes = wg.find('div', class_='columnWorkgroupsJoinCodes').text.strip()
            lic_db[name] = {"Id":wg.get("id"),"Created": creation, "Expiration": expiration,
                "Maintenance Expiry": maintenance, "Members_count": members,"Members":[], "Licenses": licenses, "Join Codes": join_codes}
        url = "https://mycentre.pscad.com/logics/ajax/workgroupMember/ajx-license-view.php"

        for each_pscad in lic_db:
            files = {
                "workgroupID": (None, lic_db[each_pscad].get("Id"))
            }
            response = session.post(url, files=files)
            json_data = response.json()
            html_data = json_data.get("layout")
            soup = BeautifulSoup(html_data, 'html.parser')
            license_groups = soup.find_all('div', class_='cardLineMulti')

            for group in license_groups:
                detail_items = group.find_all('div', class_='cardLineTwoInfoLicense')
                for detail in detail_items:
                    license_id = detail.find('div', class_='columnLicensesID').text.strip()
                    license_name = detail.find('div', class_='columnLicensesName').text.strip()
                    expiry = detail.find('div', class_='columnLicensesExpiry').text.strip()
                    machine = detail.find('div', class_='columnLicensesMachine').text.strip()
                    checked_out_by = detail.find('div', class_='columnLicensesCheckout').text.strip()
                    checkout_expiry = detail.find('div', class_='columnLicensesCheckoutExpiry').text.strip()
                    checkout_period = detail.find('div', class_='columnLicensesCheckoutPeriod').text.strip()

                    lic_db[each_pscad]["Members"].append({
                        'license_id': license_id,
                        'name': license_name,
                        'expiry': expiry,
                        'machine': machine,
                        'checked_out_by': checked_out_by,
                        'checkout_expiry': checkout_expiry,
                        'checkout_period': checkout_period
                    })
    return lic_db

if __name__ == "__main__":
    username = "your_username"
    password = "your_password"
    lic_db = get_pscad_license_usage(username, password)
    print(lic_db)



