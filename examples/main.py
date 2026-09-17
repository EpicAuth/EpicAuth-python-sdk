from epicauth import EpicAuth

import hashlib
import sys

import time
import platform
import os
from time import sleep
from datetime import datetime, UTC
import subprocess
import urllib.request
import webbrowser
import random
import string


def clear():
    if platform.system() == 'Windows':
        os.system('cls & title Python Example')  # clear console, change title
    elif platform.system() == 'Linux':
        os.system('clear')  # Clear the terminal
        sys.stdout.write("\033]0;Python Example\007")  # Set terminal title
        sys.stdout.flush() 
    elif platform.system() == 'Darwin':
        os.system("clear && printf '\033[3J'")  # Clear terminal and scrollback
        os.system('echo -n -e "\033]0;Python Example\007"')  # Set terminal title


def generate_random_string(length: int = 8) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))

def handle_auto_update(EpicAuthApp:EpicAuth):
    invalid_version_message = "invalidver"

    if EpicAuthApp.response.message != invalid_version_message:
        return

    download_link = EpicAuthApp.app_data.downloadLink

    if download_link:
        print("\n Auto update available!")
        print(" Choose how you'd like to auto update:")
        print(" [1] Open file in browser")
        print(" [2] Download file directly")

        try:
            update_choice = int(input(" > "))
        except ValueError:
            print(" Invalid selection, terminating program..")
            time.sleep(1.5)
            sys.exit(0)

        if update_choice == 1:
            webbrowser.open(download_link)
            sys.exit(0)

        elif update_choice == 2:
            print(" Downloading file directly..")
            print(" New file will be opened shortly..")

            executable_path = sys.executable

            random_suffix = generate_random_string()

            base, ext = os.path.splitext(executable_path)
            new_file_path = f"{base}-{random_suffix}{ext}"

            try:
                urllib.request.urlretrieve(
                    download_link,
                    new_file_path
                )

                subprocess.Popen([new_file_path])

                subprocess.Popen(
                    [
                        "cmd.exe",
                        "/C",
                        f'timeout /T 3 /NOBREAK >nul & del /F /Q "{executable_path}"'
                    ],
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

            except Exception as e:
                print(f" Failed to update: {e}")
                time.sleep(2)
                sys.exit(1)

            sys.exit(0)

        else:
            print(" Invalid selection, terminating program..")
            time.sleep(1.5)
            sys.exit(0)

    print(
        "\n Status: Version of this program does not match the one online. "
        "Furthermore, the download link online isn't set. "
        "You will need to manually obtain the download link from the developer."
    )



print("Initializing")

def get_checksum():
    """Return MD5 hash of current script"""
    md5_hash = hashlib.md5()
    with open(sys.argv[0], "rb") as f:
        md5_hash.update(f.read())
    return md5_hash.hexdigest()



EpicAuthApp = EpicAuth(
    name="AppName",
    ownerid="OwnerId",
    version="AppVersion",
    hash_to_check=get_checksum()
)



EpicAuthApp.init()

handle_auto_update(EpicAuthApp)

if not EpicAuthApp.response.success:
    print("\n Status: "+ EpicAuthApp.response.message)
    sys.exit(1)


def show_menu():
    print("""
1. Login
2. Register
3. Upgrade
4. License Key Only
    """)
    return input("Select Option: ").strip()


def handle_choice(choice:int, EpicAuthApp:EpicAuth):
    try:
        if choice == "1":
            user = input('Username: ')
            password = input('Password: ')
            code = input('2FA Code (optional): ')
            EpicAuthApp.login(user, password, code or None)
            return 
        elif choice == "2":
            user = input('Username: ')
            password = input('Password: ')
            license = input('License: ')
            EpicAuthApp.register(user, password, license)
            return
        elif choice == "3":
            user = input('Username: ')
            license = input('License: ')
            EpicAuthApp.upgrade(user, license)
            return
        elif choice == "4":
            key = input('License: ')
            code = input('2FA Code (optional): ')
            EpicAuthApp.license(key, code or None)
            return
        else:
            print("Invalid option")
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)


choice = show_menu()
handle_choice(choice, EpicAuthApp)

if not EpicAuthApp.response.success:
    print("\n Status: "+ EpicAuthApp.response.message)
    sys.exit(1)
    
EpicAuthApp.fetchStats()

print("\nApplication data:")
print(f"App Version: {EpicAuthApp.app_data.app_ver}")
print(f"Customer Panel: {EpicAuthApp.app_data.customer_panel}")
print(f"Keys: {EpicAuthApp.app_data.numKeys}")
print(f"Users: {EpicAuthApp.app_data.numUsers}")
print(f"Online Users: {EpicAuthApp.app_data.onlineUsers}")

print("\nUser data:")
print(f"Username: {EpicAuthApp.user_data.username}")
print(f"IP: {EpicAuthApp.user_data.ip}")
print(f"HWID: {EpicAuthApp.user_data.hwid}")

for i, sub in enumerate(EpicAuthApp.user_data.subscriptions, 1):
    expiry = datetime.fromtimestamp(int(sub["expiry"]), UTC).strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{i}] Subscription: {sub['subscription']} - Expiry: {expiry} - Timeleft: {sub['timeleft']}")


print("Created at: " + datetime.fromtimestamp(int(EpicAuthApp.user_data.createdate), UTC).strftime('%Y-%m-%d %H:%M:%S'))
print("Last login at: " + datetime.fromtimestamp(int(EpicAuthApp.user_data.lastlogin), UTC).strftime('%Y-%m-%d %H:%M:%S'))
print("Expires at: " + datetime.fromtimestamp(int(EpicAuthApp.user_data.expires), UTC).strftime('%Y-%m-%d %H:%M:%S'))

# Two Factor EpicAuthAppentication
tfa_choice = input("\nTwo Factor EpicAuthApp: 1.Enable 2FA 2.Disable 2FA\nSelect Option: ")
if tfa_choice == "1":
    EpicAuthApp.enable2fa()
elif tfa_choice == "2":
    EpicAuthApp.disable2fa()
else:
    print("Invalid Option")


print("\nExiting in five seconds..")
sleep(5)
sys.exit(1)

