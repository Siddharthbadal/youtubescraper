from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"

def get_drivers():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')

  driver = webdriver.Chrome(options = chrome_options)
  return driver

def get_videos(driver):
  driver.get(YOUTUBE_TRENDING_URL)
  print(driver.title)
  video_div_tag = 'ytd-video-renderer'
  videos = driver.find_elements(By.TAG_NAME, video_div_tag)
  return videos 

def parse_videos(video):
  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text
  url = title_tag.get_attribute('href')

  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')

  description = video.find_element(By.ID, 'description-text').text

  uploaded_on = video.find_element(By.ID, 'metadata-line').text

  channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
  channel_name = channel_div.text

  return {
    'Title': title,
    'URL': url,
    'Thumbnail': thumbnail_url,
    'Uploaded on': uploaded_on,
    "Channel Name": channel_name,
    'Description': description
  }


if __name__=="__main__":
  print("creating drivers to fetch data.. .")
  driver = get_drivers()
  print("Fetching the page.. ")
  videos = get_videos(driver)
  print(f"Found {len(videos)} videos!")

  print("Parsing the top 25 Videos")
  top_trending_videos = [parse_videos(video) for video in videos[:25]]

  print("Data saved into a CSv File!")

  videos_df = pd.DataFrame(top_trending_videos)
  print(videos_df)
  videos_df.to_csv('trendingYTVidoes.csv', index=None)
  
