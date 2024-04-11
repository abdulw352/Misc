import feedparser
import requests
from PIL import Image
import io
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

# Function to generate an image using Stable Diffusion
def generate_image(prompt):
    url = "https://api.anthropic.com/v1/complete"
    payload = {
        "model": "stable-diffusion-v1",
        "prompt": prompt,
        "num_images": 1,
        "quality_level": "best"
    }
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "YOUR_API_KEY"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        image_data = response.json()['images'][0]
        image = Image.open(io.BytesIO(image_data))
        return image
    else:
        print(f"Error generating image: {response.text}")
        return None

# Function to post an image to Instagram
def post_to_instagram(image, caption):
    api = InstagramAPI("YOUR_USERNAME", "YOUR_PASSWORD")
    api.login()
    api.uploadPhoto(image, caption=caption)

# Main script
trending_topics = get_trending_topics(rss_feeds)
print(f"Trending topics: {', '.join(trending_topics)}")

for topic in trending_topics:
    prompt = f"A highly detailed image of {topic}"
    image = generate_image(prompt)
    if image:
        print(f"Generated image for topic: {topic}")
        image.show()
        caption = f"Image generated for the trending topic '{topic}'"
        post_to_instagram(image, caption)
