import requests
from bs4 import BeautifulSoup
import os

# Your HTML snippet
html = '''
<div class="col-xs-10 ProductImage__preview-container___2oTeX" tabindex="0"><div style="cursor:crosshair;width:auto;height:auto;font-size:0px;position:relative;-webkit-user-select:none"><img src="https://onemg.gumlet.io/l_watermark_346,w_690,h_700/a_ignore,w_690,h_700,c_pad,q_auto,f_auto/ed7141770f184a17bc8ca72aafdfeac8.jpg" alt="" style="max-width:max-content;max-height:350px;display:block;margin:auto;width:100%;height:auto;pointer-events:none"><div><div style="width: 100%; height: 0px; inset: 0px auto auto; display: block; background-color: rgba(0, 0, 0, 0.4); position: absolute; transform: translate(0px, 0px); opacity: 0; transition: opacity 300ms ease-in;"></div><div style="width: 66px; height: 108px; inset: 0px auto auto 0px; display: block; background-color: rgba(0, 0, 0, 0.4); position: absolute; transform: translate(0px, 0px); opacity: 0; transition: opacity 300ms ease-in;"></div><div style="width: 119px; height: 108px; inset: 0px 0px auto auto; display: block; background-color: rgba(0, 0, 0, 0.4); position: absolute; transform: translate(0px, 0px); opacity: 0; transition: opacity 300ms ease-in;"></div><div style="width: 100%; height: 185px; inset: 108px auto auto; display: block; background-color: rgba(0, 0, 0, 0.4); position: absolute; transform: translate(0px, 0px); opacity: 0; transition: opacity 300ms ease-in;"></div></div></div></div>
'''

# Extract image URL
soup = BeautifulSoup(html, 'html.parser')
img_tag = soup.find('img')
img_url = img_tag['src'] if img_tag else None

if img_url:
    # Download image
    response = requests.get(img_url, stream=True)
    if response.status_code == 200:
        # Save to local file
        filename = os.path.basename(img_url.split('/')[-1])
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Image saved as {filename}")
    else:
        print(f"Failed to download image: {response.status_code}")
else:
    print("No image found in HTML.")
