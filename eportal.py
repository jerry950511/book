import requests
from bs4 import BeautifulSoup
import json

class login:
    def __init__(self,account,password):
        response = requests.get("https://wane.nutc.edu.tw/dm_device/device1.php?eportal_id="+account+"&eportal_passwd="+password+"&out=mem_check")

        text = response.text
        
        pretext = ')]}\''
        text = text.replace(pretext,'')
        # 把字串讀取成json
        self.soup = json.loads(text)
    def get_info(self):
        if self.soup["res_echo"] == "pass":
            return {"stId":"s"+self.soup["st_id"],"stName":self.soup["st_name"],"status":"success"}
        else:
            return {"status":"error"}