# YT-Channel-Analytics

##  Overview
YT-Channel-Analytics is a Python-based tool that fetches and visualizes the most viewed videos from a given YouTube channel. The project leverages the YouTube Data API to retrieve video statistics and presents the data in an interactive, visually appealing HTML dashboard.

##  Features
-  Fetches the **most viewed videos** of a YouTube channel
-  Interactive **bar chart** using Plotly
-  **Clickable video links** for easy access
-  **Video statistics** (views, likes, comments)
-  **Dark-themed UI** for a modern look
-  HTML report with an **embedded graph and video list**

##  Installation
1. **Clone the repository**
   ```sh
   git clone https://github.com/Fyiss/YT-Channel-Analytics.git
   cd YT-Channel-Analytics
   ```
2. **Install dependencies**
   ```sh
   pip install requests pandas plotly
   ```
3. **Set up YouTube API Key**
   - Get a YouTube Data API key from Google Developer Console
   - Replace `API_KEY = "your_api_key_here"` in `youtube_analysis.py`

##  Usage
Run the script to generate an interactive report:
```sh
python3 youtube_analysis.py
```
This will:
- Fetch **top videos**
- Generate an **HTML dashboard**
- Open it automatically in the browser

##  Contributing
Pull requests are welcome! If you have suggestions, feel free to open an issue.

