import requests


class Crumbl:

    def __init__(self):
        self.cookie_name_str = 'individual-cookie-flavor-'
        self.image_file_types = ['.jpg', '.png']
        self.cookie_names = None
        self.cookie_image_urls = None

    def get_cookies(self):
        req = requests.get('https://crumblcookies.com')
        content = req.content

        content_str = str(content)

        #  Get names
        content_str_broken_for_name = content_str.split(self.cookie_name_str)
        num_cookies = len(content_str_broken_for_name) - 1
        self.cookie_names = [content_str_broken_for_name[i][:content_str_broken_for_name[i].find('"')] for i in range(1, num_cookies + 1)]

        #  Clean up the cookie names (sometimes they have parenthesis containing ugly byte information)
        for i, cookie_name in enumerate(self.cookie_names):
            if "(" in cookie_name:
                cookie_name = cookie_name.split("(")[0][:-1]
                self.cookie_names[i] = cookie_name


        #  Get images
        self.cookie_image_urls = []
        for i in range(1, num_cookies + 1):
            for img_type in self.image_file_types:
                if img_type in content_str_broken_for_name[i]:
                    img_url = content_str_broken_for_name[i].split(img_type)[0].split('https://')[-1]
                    img_url = 'https://' + img_url + img_type
                    # print(img_url)
                    if self.cookie_names[i - 1].replace(' ', '')[:5] in img_url:  # Check if the first 5 chars of the cookie name match in the image
                        self.cookie_image_urls.append(img_url)
                    continue


    def save_cookies(self, dir):
        for i in range(len(self.cookie_names)):
            img_type = self.cookie_image_urls[i][-4:]
            with open(dir + '/' + self.cookie_names[i].replace(' ', '') + img_type, 'wb') as file:
                file.write(requests.get(self.cookie_image_urls[i]).content)




if __name__ == "__main__":
    crumbl = Crumbl()
    crumbl.get_cookies()
    crumbl.save_cookies('resources/crumbl/')





