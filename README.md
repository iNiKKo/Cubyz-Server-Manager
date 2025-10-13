# 🚀 Website-based **Cubyz Player Count & Player Names** (BETA)

---

## ⚙️ How it works  
The **Python script** reads your server logs to track who joined or left the game.  
It also **removes symbols and color codes** from player names to keep it clean and readable.

---

## 🎉 Finished Product  
Check it out here: [https://status.ashframe.net/](https://status.ashframe.net/)

---

## 📚 Tutorial *(Under Development)*

> **Note:** This tutorial is based on **Debian Linux**

Prerequisites
- Ngrock (Port Forwarding to 5000)
- Python3
- Domain Name preferebly Cloudflare based (should work with Public IP but NOT reccomended and no tutorial)

1. **Port forward** TCP port **5000** and your game’s UDP port in your router  
2. **Download** the Python script from GitHub  
3. **Place** the Python script inside the **Logs folder** of your Cubyz server  
4. **Edit** the Python script:  
   - On **line 10**, update the path to your `latest.log` file  
5. Save & Run
6. Follow these Instructions https://ngrok.com/download/linux?tab=install (egister and then ngrok http 5000)
7. Take the new HTTPS address from Ngrock and Download Index.html where you need to change Address at line 17 & 24
8. Create a new Github Repo, uplaod the Index.html go into Settings / Pages and set branch to main or root
9. After a minute you should be able to access your website https://PROFILE_NAME.github.io/YOUR-REPO-HERE/

---

*More coming soon!*
