import urllib.request
from html.parser import HTMLParser


class NestedParser(HTMLParser):
    def __init__(self, target_id):
        super().__init__()
        self.target_id = target_id
        self.found_announce = False
        self.depth_count = 0
        self.target_depth = 3
        self.result_text = None
        self.capture_text = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # 1. Look for the element with id='announce'
        if attrs_dict.get("id") == self.target_id:
            self.found_announce = True
            return

        # 2. If we are inside 'announce', track the first nested child for 3 iterations
        if self.found_announce and self.depth_count < self.target_depth:
            self.depth_count += 1
            if self.depth_count == self.target_depth:
                self.capture_text = True

    def handle_data(self, data):
        # 3. Get the text of the 3rd nested element
        if self.capture_text and self.result_text is None:
            self.result_text = data.strip()


def scrape_nested_element(url):
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode("utf-8")

        parser = NestedParser("announce")
        parser.feed(html_content)

        return parser.result_text
    except Exception as e:
        return f"Error: {e}"


# Usage
print(scrape_nested_element("https://underground.boardhost.com/index.php"))
