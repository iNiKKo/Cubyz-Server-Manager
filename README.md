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
5. **Save** the changes and **run** the Python script.

6. **Set up ngrok:**
   - Follow the installation instructions for Linux: [https://ngrok.com/download/linux?tab=install](https://ngrok.com/download/linux?tab=install)
   - Register for an ngrok account if you haven't already.
   - Start a tunnel by running:
     ```bash
     ngrok http 5000
     ```
   - Copy the HTTPS URL provided by ngrok.

7. **Download** the `index.html` file and update it:
   - Open the file in any text editor.
   - Replace the ngrok URL on **line 17** and **line 24** with your newly generated HTTPS URL.
   - Save the file.

8. **Create a new GitHub repository:**
   - Upload the updated `index.html` file to your repo.
   - Navigate to **Settings > Pages**.
   - Set the source to the `main` branch and the folder to `/ (root)`.

9. **Access your website:**
   - After about a minute, your site should be live at:
     ```
     https://<YOUR-GITHUB-USERNAME>.github.io/<YOUR-REPO-NAME>/

---

*More coming soon!*
