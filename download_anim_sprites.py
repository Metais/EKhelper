import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# URL of the webpage with animations
url = 'https://www.pokencyclopedia.info/en/index.php?id=sprites/gen3/ani_emerald'

# Fetch the webpage content
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all <img> tags with relative src containing .gif extension
animation_tags = soup.find_all('img', src=lambda src: src and src.endswith('.gif'))

# Create a directory to save the animations
create_directory('animations')

# Download each animation
for index, animation_tag in enumerate(animation_tags, start=1):
    if index == 1:
        continue
    animation_url = urljoin(url, animation_tag['src'])
    animation_name = animation_tag['alt'].split(' ')[1] + '.gif'
    animation_path = os.path.join('animations', animation_name)

    # Download the animation
    with open(animation_path, 'wb') as f:
        animation_response = requests.get(animation_url)
        f.write(animation_response.content)

    print(f'Downloaded animation {index}: {animation_name}')

print('All animations downloaded successfully!')