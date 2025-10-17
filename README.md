# 🚀 **Cubyz Server Manager**

---

## ⚙️ How it works  

This Python script monitors your server logs to track player activity — including **joins**, **leaves**, and **deaths**.  
It also **cleans up player names** by removing symbols and color codes for better readability.  
Additionally, it keeps track of your **server IP** and **icon URL** to send data to a connected website.


---

## 📚 Tutorial

## Prerequisites
- `Python 3`
- `requests`

```bash
sudo apt update && sudo apt install -y python3 python3-pip
```
```bash
pip3 install requests
```
---

## 📥 Setup Instructions

1. **Download the script**  
   - [`csm.py`](https://github.com/iNiKKo/cubyz-server-list/blob/main/Scripts/csm.py)

2. **Place the script in your server’s log folder**  
   This should be the folder that contains `latest.log`.

3. **Edit the script**
   - Change all of these. 
     Example:
     ```python
     LOG_PATH = "/FULL/PATH/TO/LOGS/latest.log"
     SERVER_ID = "YOUR_SERVER_NAME_KEEP_IT_SHORT"
     SERVER_IP = "YOUR_SERVER_IP_ADDRESS"
     ICON_URL = "URL_FOR_ICON" 
     GAMEMODE = "survival"
     ```

4. **Run the script**
```bash
python3 csm.py
```
> **Note:** You **must** launch the game **first**, then run `csm.py`, and only **after that**, open your server.
---
