import os
import sys
import json
import time
import platform
import subprocess
import binascii
from datetime import datetime, timezone, timedelta

import requests
import qrcode
from PIL import Image
from discord_interactions import verify_key


if os.name == "nt":
    import win32security

class EpicAuthError(Exception):
    pass

class EpicAuth:
    baseUrl = "https://EpicAuth.cc/api/1.3/"

    def __init__(self, name: str, ownerid: str, version: str, hash_to_check: str):
        if len(ownerid) != 10:
            raise ValueError("EpicAuth: ownerid must be exactly 10 characters")

        self.name = name
        self.ownerid = ownerid
        self.version = version
        self.hash_to_check = hash_to_check

    sessionid = enckey = ""
    initialized = False
    def init(self):
        if self.initialized:
            raise RuntimeError("EpicAuth already initialized")

        payload = {
            "type": "init",
            "ver": self.version,
            "hash": self.hash_to_check,
            "name": self.name,
            "ownerid": self.ownerid,
        }

        response = self.__do_request(payload)

        if response == "EpicAuth_Invalid":
            raise RuntimeError("EpicAuth: application not found")

        data = json.loads(response)
        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)

        self.load_response_struct(data)
        if data.get("success"):
            self.sessionid = data["sessionid"]
            self.initialized = True
        if data.get("message") == "invalidver":
            self.app_data.downloadLink = data.get('download') or ""


    def register(self, user, password, license, hwid=None):
        self.checkinit()

        if hwid is None:
            hwid = others.get_hwid()

        payload = {
            "type": "register",
            "username": user,
            "pass": password,
            "key": license,
            "hwid": hwid,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(payload)
        data = json.loads(response)
        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)

        self.load_response_struct(data)
        if data.get("success"):
            self.__load_user_data(data["info"])
        if data.get("message") == "invalidver":
            self.app_data.downloadLink = data.get('download') or ""

    def upgrade(self, user, license):
        self.checkinit()

        payload = {
            "type": "upgrade",
            "username": user,
            "key": license,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(payload)
        data = json.loads(response)

        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)
        self.load_response_struct(data)
        if data.get("success"):
            self.__load_user_data(data["info"])
        if data.get("message") == "invalidver":
            self.app_data.downloadLink = data.get('download') or ""
      


    def login(self, user, password, code=None, hwid=None):
        self.checkinit()

        if hwid is None:
            hwid = others.get_hwid()

        payload = {
            "type": "login",
            "username": user,
            "pass": password,
            "hwid": hwid,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid,
        }

        if code is not None:
            payload["code"] = code

        response = self.__do_request(payload)
        data = json.loads(response)
        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)
        self.load_response_struct(data)
        if data.get("success"):
            self.__load_user_data(data["info"])
        if data.get("message") == "invalidver":
            self.app_data.downloadLink = data.get('download') or ""

    def license(self, key, code=None, hwid=None):
        self.checkinit()

        if hwid is None:
            hwid = others.get_hwid()

        payload = {
            "type": "license",
            "key": key,
            "hwid": hwid,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        if code is not None:
            payload["code"] = code

        response = self.__do_request(payload)
        data = json.loads(response)
        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)
        self.load_response_struct(data)
        if data.get("success"):
            self.__load_user_data(data["info"])
        if data.get("message") == "invalidver":
            self.app_data.downloadLink = data.get('download') or ""


    def var(self, name)->str | None:
        self.checkinit()

        payload = {
            "type": "var",
            "varid": name,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(payload)
        data = json.loads(response)
        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)
        self.load_response_struct(data)
        if data.get("success"):
            return data["message"]
        return None


    def getvar(self, var_name)-> str|None:
        self.checkinit()

        payload = {
            "type": "getvar",
            "var": var_name,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(payload)
        data = json.loads(response)

        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)
        self.load_response_struct(data)
        if data.get("success"):
            return data["message"]
        return None

        #  print(f"NOTE: This is commonly misunderstood. This is for user variables, not the normal variables.\nUse EpicAuthapp.var(\"{var_name}\") for normal variables");

    def setvar(self, var_name, var_data)->None:
        self.checkinit()

        payload = {
            "type": "setvar",
            "var": var_name,
            "data": var_data,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }
        response = self.__do_request(payload)
        data = json.loads(response)

        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)
        self.load_response_struct(data)


    def ban(self)->None:
        self.checkinit()

        payload = {
            "type": "ban",
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }
        response = self.__do_request(payload)

        data = json.loads(response)
        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)
        self.load_response_struct(data)

    def file(self, fileid)->bytes:
        self.checkinit()

        payload = {
            "type": "file",
            "fileid": fileid,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(payload)

        data = json.loads(response)
        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)

        self.load_response_struct(data)
        if data.get("success"):
            return binascii.unhexlify(data["contents"])
        return b""
            

       

    def webhook(self, webid, param, body = "", conttype = "")->str:
        self.checkinit()

        payload = {
            "type": "webhook",
            "webid": webid,
            "params": param,
            "body": body,
            "conttype": conttype,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(payload)

        data = json.loads(response)

        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)

        self.load_response_struct(data)
        if self.response.success:
            return data.get("response", "")
        return ""


    def check(self):
        self.checkinit()

        payload = {
            "type": "check",
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }
        response = self.__do_request(payload)

        data = json.loads(response)
        self.load_response_struct(data)

        if self.response.success:
            return True
        else:
            return False

    def checkblacklist(self):
        self.checkinit()
        hwid = others.get_hwid()

        payload = {
            "type": "checkblacklist",
            "hwid": hwid,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }
        response = self.__do_request(payload)

        data = json.loads(response)
        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)

        self.load_response_struct(data)

        if self.response.success:
            return True
        else:
            return False

    def log(self, message):
        self.checkinit()

        payload = {
            "type": "log",
            "pcuser": os.getenv('username'),
            "message": message,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        self.__do_request(payload)


    def fetchOnline(self):
        self.checkinit()

        payload = {
            "type": "fetchOnline",
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(payload)

        data = json.loads(response)
        self.load_response_struct(data)

        if self.response.success:
            return data.get("users", [])
        
        return None
            
    def fetchStats(self):
        self.checkinit()

        payload = {
            "type": "fetchStats",
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(payload)

        data = json.loads(response)
        self.load_response_struct(data)
        if self.response.success:
            self.__load_app_data(data["appinfo"])
            
    def chatGet(self, channel):
        self.checkinit()

        payload = {
            "type": "chatget",
            "channel": channel,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(payload)

        data = json.loads(response)
        self.load_response_struct(data)
        if self.response.success:
            return data["messages"]
        else:
            return None

    def chatSend(self, message, channel):
        self.checkinit()

        payload = {
            "type": "chatsend",
            "message": message,
            "channel": channel,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(payload)

        data = json.loads(response)
        self.load_response_struct(data)
        if self.response.success:
            return True
        else:
            return False

    def checkinit(self):
        if not self.initialized:
            raise RuntimeError("You must run the function EpicAuthApp.init(); first")

    def changeUsername(self, username):
        self.checkinit()

        payload = {
            "type": "changeUsername",
            "newUsername": username,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(payload)

        data = json.loads(response)
        self.load_response_struct(data)

    def logout(self):
        self.checkinit()

        payload = {
            "type": "logout",
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(payload)

        data = json.loads(response)
        self.load_response_struct(data)
        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)

        return None   
 
            
    def enable2fa(self, code=None):
        self.checkinit()
        
        payload = {
            "type": "2faenable",
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid,
            "code": code
        }       
        
        response = self.__do_request(payload)
        
        data = json.loads(response)
        self.load_response_struct(data)
        isOwnerIdValid = data.get("ownerid") == self.ownerid
        if not isOwnerIdValid:
            sys.exit(1)
        if self.response.success:
            if code is None:
                # First request: Display the 2FA secret code
                print(f"Your 2FA secret code is: {data['2fa']['secret_code']}")
                qr_code = data['2fa']['QRCode']
                self.display_qr_code(qr_code)
                code_input = input("Enter the 6 digit authentication code from your authentication app: ")
                self.enable2fa(code_input)
            else:
                # Second request: Confirm successful 2FA activation
                print("2FA has been successfully enabled!")
                time.sleep(3)
        else:
             raise EpicAuthError(data.get("message"))
             
            
    def disable2fa(self, code=None):
        self.checkinit()
        
        code = input("Enter the 6 digit 2fa code to disable 2fa: ")
        
        payload = {
            "type": "2fadisable",
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid,
            "code": code
        }
        
        response = self.__do_request(payload)
        
        data = json.loads(response)
        self.load_response_struct(data)
        return(self.response.message)

        
            
    def display_qr_code(self, qr_code_url):
            # Generate QR code image
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            # Add the QR code URL data
            qr.add_data(qr_code_url)
            qr.make(fit=True)

            # Create an image from the QR code
            img = qr.make_image(fill='black', back_color='white')

            # Display the QR code image
            img.show()            
            
    def __do_request(self, payload):
        try:
            response = requests.post(
                EpicAuth.baseUrl, data=payload, timeout=10
            )

            if payload["type"] == "log" or payload["type"] == "file" or payload["type"] == "2faenable" or payload["type"] == "2fadisable":
                return response.text
            
            # Get the signature and timestamp from the headers
            signature = response.headers.get("x-signature-ed25519")
            timestamp = response.headers.get("x-signature-timestamp")

            if not signature or not timestamp:
                raise EpicAuthError("Missing headers for signature verification.")


            server_time = datetime.fromtimestamp(int(timestamp), timezone.utc)
            current_time = datetime.now(timezone.utc)
            
            #print(f"Server Timestamp (UTC seconds): {timestamp}")
            #print(f"Server Time (UTC seconds): {server_time.timestamp()}")
            #print(f"Current Time (UTC seconds): {current_time.timestamp()}")

            buffer_seconds = 5
            time_difference = current_time - server_time

            if time_difference > timedelta(seconds=20 + buffer_seconds):
                raise EpicAuthError("Timestamp is too old (exceeded 20 seconds + buffer).")


            if not verify_key(response.text.encode('utf-8'), signature, timestamp, '95b38710f40927b16528a073b87d942e03bd4578d49963a19ebae177945f89ac'):
                raise EpicAuthError("Signature checksum failed. Request was tampered with or session ended most likely.")


            return response.text

        except requests.exceptions.Timeout: 
            raise EpicAuthError("Request timed out. Server is probably down/slow at the moment")
                
            


    class application_data_class:
        numUsers = numKeys = app_ver = customer_panel = downloadLink = onlineUsers = ""

    class user_data_class:
        username = ip = hwid = expires = createdate = lastlogin = subscription = subscriptions = ""
    class Response_class:
        success = False
        message = ""

    user_data = user_data_class()
    app_data = application_data_class()
    response = Response_class()

    def __load_app_data(self, data):
        self.app_data.numUsers = data["numUsers"]
        self.app_data.numKeys = data["numKeys"]
        self.app_data.app_ver = data["version"]
        self.app_data.customer_panel = data["customerPanelLink"]
        self.app_data.onlineUsers = data["numOnlineUsers"]

    def __load_user_data(self, data):
        self.user_data.username = data["username"]
        self.user_data.ip = data["ip"]
        self.user_data.hwid = data["hwid"] or "N/A"
        self.user_data.expires = data["subscriptions"][0]["expiry"]
        self.user_data.createdate = data["createdate"]
        self.user_data.lastlogin = data["lastlogin"]
        self.user_data.subscription = data["subscriptions"][0]["subscription"]
        self.user_data.subscriptions = data["subscriptions"]

    def load_response_struct(self, data):
        self.response.success = data.get("success", False)
        self.response.message = data.get("message", "")


class others:
    @staticmethod
    def get_hwid():
        if platform.system() == "Linux":
            with open("/etc/machine-id") as f:
                hwid = f.read()
                return hwid
        elif platform.system() == 'Windows':
            winuser = os.getlogin()
            sid = win32security.LookupAccountName(None, winuser)[0]  # You can also use WMIC (better than SID, some users had problems with WMIC)
            hwid = win32security.ConvertSidToStringSid(sid)
            return hwid
            '''
            cmd = subprocess.Popen(
                "wmic useraccount where name='%username%' get sid",
                stdout=subprocess.PIPE,
                shell=True,
            )

            (suppost_sid, error) = cmd.communicate()

            suppost_sid = suppost_sid.split(b"\n")[1].strip()

            return suppost_sid.decode()

            ^^ HOW TO DO IT USING WMIC
            '''
        elif platform.system() == 'Darwin':
            output = subprocess.Popen("ioreg -l | grep IOPlatformSerialNumber", stdout=subprocess.PIPE, shell=True).communicate()[0]
            serial = output.decode().split('=', 1)[1].replace(' ', '')
            hwid = serial[1:-2]
            return hwid