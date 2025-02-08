import requests
import pandas as pd
import plotly.express as px
import webbrowser
import textwrap


API_KEY = "Enter-API-KEY-HERE"
CHANNEL_ID = "Enter Channel ID here"

def get_channel_name(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?key={API_KEY}&id={channel_id}&part=snippet"
    response = requests.get(url).json()
    return response["items"][0]["snippet"]["title"] if "items" in response else "Unknown Channel"

def get_most_viewed_videos(channel_id, max_results=10):
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=snippet,id&order=viewCount&maxResults={max_results}"
    response = requests.get(url).json()
    
    video_data = []
    for item in response.get("items", []):
        if item["id"].get("videoId"):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"].replace("$", "USD")  
            stats = get_video_stats(video_id)
            video_data.append({"title": title, "video_id": video_id, **stats})
    
    df = pd.DataFrame(video_data)
    return df.sort_values(by="views", ascending=False)  


def get_video_stats(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&id={video_id}&part=statistics"
    response = requests.get(url).json()
    stats = response.get("items", [{}])[0].get("statistics", {})
    
    return {
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats.get("likeCount", 0)),
        "comments": int(stats.get("commentCount", 0))
    }


channel_name = get_channel_name(CHANNEL_ID)


df = get_most_viewed_videos(CHANNEL_ID, max_results=10)


df["short_title"] = df["title"].apply(lambda x: "<br>".join(textwrap.wrap(x, width=40)))


df["video_url"] = "https://www.youtube.com/watch?v=" + df["video_id"]


fig = px.bar(df, 
             x="views", 
             y="short_title", 
             title=f"📊 {channel_name} - Most Viewed YouTube Videos",
             orientation="h",
             color="views",
             color_continuous_scale="plasma",  
             hover_data={"title": True, "likes": True, "comments": True, "video_url": True})  

fig.update_layout(yaxis_categoryorder="total ascending",  
                  plot_bgcolor="black", 
                  paper_bgcolor="black",
                  font=dict(color="white"))


df["clickable_title"] = df.apply(lambda row: f"<a href='{row['video_url']}' target='_blank'>{row['title']}</a>", axis=1)


fig.write_html("youtube_analysis.html")


html_table = df[["clickable_title", "views", "likes", "comments"]].to_html(escape=False, index=False)


final_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Analysis</title>
    <style>
        body {{ background-color: black; color: white; font-family: Arial, sans-serif; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #222; }}
        th, td {{ border: 1px solid white; padding: 10px; text-align: left; }}
        th {{ background-color: #444; }}
        a {{ color: cyan; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>{channel_name} - Most Viewed YouTube Videos</h1>
    <iframe src="youtube_analysis.html" width="100%" height="600px"></iframe>
    <h2>Clickable List of Videos</h2>
    {html_table}
</body>
</html>
"""


with open("youtube_clickable.html", "w") as f:
    f.write(final_html)


webbrowser.open("youtube_clickable.html")

