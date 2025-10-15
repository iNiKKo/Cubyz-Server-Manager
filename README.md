# 🚀 **Cubyz Server List** (BETA)

---

## ⚙️ How it works  
The **Python script** reads your server logs to track who joined/left or died.
It also **removes symbols and color codes** from player names to keep it clean and readable.

> **Note:** some names may show up weird due to the limitations of log reading.
---

## 🎉 Finished Product  
Check it out here: [https://status.ashframe.net/](https://status.ashframe.net/)

---

## 📚 Tutorial

> **Note:** This tutorial is based on **Debian Linux**

## 🔧 Prerequisites
- `Python 3`
- The `requests` module (all others are part of Python's standard library)

---

## 📥 Setup Instructions

1. **Download the script**  
   - [`csm.py`](https://github.com/iNiKKo/cubyz-server-list/blob/main/Scripts/csm.py)

2. **Place the script in your server’s log folder**  
   This should be the folder that contains `latest.log`.

3. **Edit the script**
   - Line `8`: Set the path to your `latest.log`  
     Example:
     ```python
     log_path = "/home/youruser/server/logs/latest.log"
     ```
   - Line `9`: Set a unique server ID  
     Example:
     ```python
     SERVER_ID = "Your_Server_Name"
     ```

4. **Run the script**
```bash
python3 csm.py
```

---
