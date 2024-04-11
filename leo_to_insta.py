import feedparser
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from instagram_api import InstagramAPI

# Define the list of RSS feeds to explore
rss_feeds = [
    'https://example.com/feed1.rss',
    'https://example.com/feed2.rss',
    # Add more RSS feed URLs here
]

# Function to find the most common words in the RSS feed entries
def get_trending_topics(rss_feeds):
    word_frequency = {}
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            words = entry.title.split() + entry.description.split()
            for word in words:
                word_frequency[word] = word_frequency.get(word, 0) + 1
    sorted_words = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    trending_topics = [word for word, _ in sorted_words[:10]]
    return trending_topics

# Function to generate an image using leonardo.ai
def generate_image(prompt):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.leonardo.ai/")

    # Wait for the page to load and locate the input field
    input_field = driver.find_element_by_xpath("//input[@placeholder='Start typing your prompt']")
    input_field.send_keys(prompt)

    # Click the "Generate" button
    generate_button = driver.find_element_by_xpath("//button[contains(text(), 'Generate')]")
    generate_button.click()

    # Wait for the image to be generated
    time.sleep(30)  # Adjust the sleep time as needed

    # Save the generated image
    image_element = driver.find_element_by_xpath("//img[@class='final-image']")
    image_url = image_element.get_attribute("src")
    image_data = requests.get(image_url).content

    # Close the browser
    driver.quit()

    return image_data

# Function to post an image to Instagram
def post_to_instagram(image_data, caption):
    api = InstagramAPI("YOUR_USERNAME", "YOUR_PASSWORD")
    api.login()
    api.uploadPhoto(image_data, caption=caption)

# Main script
trending_topics = get_trending_topics(rss_feeds)
print(f"Trending topics: {', '.join(trending_topics)}")

for topic in trending_topics:
    prompt = f"A highly detailed image of {topic}"
    image_data = generate_image(prompt)
    if image_data:
        print(f"Generated image for topic: {topic}")
        caption = f"Image generated for the trending topic '{topic}'"
        post_to_instagram(image_data, caption)
