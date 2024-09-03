import http.client
import re
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

def get_latest_stories():
    
    connection = http.client.HTTPSConnection("time.com")
    connection.request("GET", "/")
    
    response = connection.getresponse()
    html_content = response.read().decode('utf-8')
    
    connection.close()

    pattern = r'<a[^>]+href="(/[^"]+)"[^>]*?>\s*<h[2-3][^>]*?>([^<]+)</h[2-3]>'
    
    matches = re.findall(pattern, html_content, re.DOTALL)
    
    stories = []
    for match in matches:
        link, title = match
    
        full_link = f"https://time.com{link}"
        
        stories.append({
            "title": title.strip(),
            "link": full_link.strip()
        })

        if len(stories) == 6:
            break
    
    return stories

# HTML template for displaying stories
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Time.com</title>
    <style>
        h1{{
            color:green;
            text-align:center;
        }}
        body {{
            font-family:'Times New Roman', Times, serif;
            background-color: gainsboro;
            margin: 0;
            padding: 20px;
            background:url("https://plus.unsplash.com/premium_photo-1661255378914-d0934128d91d?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        }}
        .stories-container{{
            display:flex;
            flex-wrap:wrap;
            gap:10px; 
        }}
        .story-container {{
            background-color:rgb(173 245 238 / 96%);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            width:600px; 
               
        }}
        .story-title {{
            font-size: 20px;
            color: black;
        }}
        .story-link {{
            font-size: 14px;
            color: #0073e6;
            text-decoration: none;
        }}
        .story-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>Latest Stories from Time.com</h1>
    <div class="stories-container" id="stories"></div>
    <script>
        const stories = JSON.parse('{stories_json}');
        const storiesDiv = document.getElementById('stories');
        
        stories.forEach(story => {{
            const storyDiv = document.createElement('div');
            storyDiv.className = 'story-container';

            const storyTitle = document.createElement('p');
            storyTitle.className = 'story-title';
            storyTitle.textContent = story.title;  

            const storyLink = document.createElement('a');
            storyLink.className = 'story-link';
            storyLink.href = story.link; 
            storyLink.textContent = story.link;  

            storyDiv.appendChild(storyTitle);
            storyDiv.appendChild(storyLink);

            storiesDiv.appendChild(storyDiv);
        }});
    </script>
</body>
</html>
"""

# HTTP Request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/getTimeStories':
            
            stories = get_latest_stories()
            
            stories_json = json.dumps(stories).replace("'", "\\'")
            
            html_content = HTML_TEMPLATE.format(stories_json=stories_json)
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=1000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run(port=1000)
