import requests
import copy

class Crumbl:

    def __init__(self):
        self.cookie_name_str = 'individual-cookie-flavor-'
        self.image_file_types = ['.jpg', '.png']
        self.cookie_names = None
        self.cookie_image_urls = None

        self.mystery_cookie = False

    def get_cookies(self):
        req = requests.get('https://crumblcookies.com')
        content = req.content

        content_str = str(content)

        #  Get names
        content_str_broken_for_name = content_str.split(self.cookie_name_str)
        num_cookies = len(content_str_broken_for_name) - 1
        self.cookie_names = [content_str_broken_for_name[i][:content_str_broken_for_name[i].find('"')].rstrip() for i in range(1, num_cookies + 1)]
        self.cookie_image_names = copy.deepcopy(self.cookie_names)

        print("names:", self.cookie_names)
        #  Clean up the cookie names (sometimes they have parenthesis containing ugly byte information/delete "mystery cookie")
        for i, cookie_name in enumerate(self.cookie_names):
            # print("Cleaning:", cookie_name)

            if "amp;" in cookie_name:
                self.cookie_names[i] = self.cookie_names[i].replace('amp;', '')
                self.cookie_image_names[i] = self.cookie_image_names[i].replace("amp;", '')
            elif "&#x27;" in cookie_name:
                self.cookie_names[i] = self.cookie_names[i].replace("&#x27;", '')
                self.cookie_image_names[i] = self.cookie_image_names[i].replace("&#x27;", '')

            if "Chocolate Peanut Butter (ft. OREO" in cookie_name:
                self.cookie_names[i] = "Chocolate Peanut Butter ft Oreo"
                self.cookie_image_names[i] = "Chocolate Peanut Butter ft Oreo"

            #  Last ditch ( cleaning
            if "(" in cookie_name:
                cookie_name = cookie_name.split("(")[0][:-1]
                self.cookie_names[i] = cookie_name.rstrip()


        print("names cleaned:", self.cookie_names)

        if "Mystery Cookie" in self.cookie_names:
            self.cookie_names.remove("Mystery Cookie")
            num_cookies -= 1
            self.mystery_cookie = True

        if "Frosted Strawberry" in self.cookie_names:
            index = self.cookie_names.index("Frosted Strawberry")
            self.cookie_names[index] = "Frosted Strawberry ft. Pop-Tart"
            self.cookie_image_names[index] = "Frosted Strawberry Pop Tarts"

        if "Peaches & Cream" in self.cookie_names:
            index = self.cookie_names.index("Peaches & Cream")
            self.cookie_names[index] = "Peaches & Cream"
            self.cookie_image_names[index] = "Peaches Cream"

        if "Strawberry Milk ft." in self.cookie_names:
            index = self.cookie_names.index("Strawberry Milk ft.")
            self.cookie_names[index] = "Strawberry Milk"
            self.cookie_image_names[index] = "Strawberry Milk"

        if "Milk Chocolate Chip" in self.cookie_names:
            index = self.cookie_names.index("Milk Chocolate Chip")
            self.cookie_names[index] = "Chocolate Chip"
            self.cookie_image_names[index] = "Chocolate Chip"

        if "Cookie Butter Lava" in self.cookie_names:
            index = self.cookie_names.index("Cookie Butter Lava")
            self.cookie_names[index] = "Biscoff Lava"
            self.cookie_image_names[index] = "Biscoff Lava"

        if "Oatmeal Mallow Sandwich" in self.cookie_names:
            index = self.cookie_names.index("Oatmeal Mallow Sandwich")
            self.cookie_names[index] = "Oatmeal Mallow Sandwich"
            self.cookie_image_names[index] = "Oatmeal Cream Sandwich"

        if "Peanut Butter Munch" in self.cookie_names:
            index = self.cookie_names.index("Peanut Butter Munch")
            self.cookie_names[index] = "Peanut Butter Munch"
            self.cookie_image_names[index] = "Muddy Buddy"

        if "Chocolate Green Mint" in self.cookie_names:
            index = self.cookie_names.index("Chocolate Green Mint")
            self.cookie_names[index] = "Chocolate Green Mint ft Andes"
            self.cookie_image_names[index] = "GreenMint"

        if "Chocolate Peanut Butter Puffs" in self.cookie_names:
            print("CHANGING")
            index = self.cookie_names.index("Chocolate Peanut Butter Puffs")
            self.cookie_image_names[index] = "PeanutButterMilkftReesesPuffs"

        if "Chocolate Peanut Butter ft Oreo" in self.cookie_names:
            print("CHANGING")
            index = self.cookie_names.index("Chocolate Peanut Butter ft Oreo")
            self.cookie_names[index] = "Chocolate Peanut Butter ft Oreo"
            self.cookie_image_names[index] = "Chocolate Peanut Butter ft Oreo"

        if "Caramel Pumpkin Cake" in self.cookie_names:
            print("CHANGING")
            index = self.cookie_names.index("Caramel Pumpkin Cake")
            self.cookie_image_names[index] = "Caramel Pumpkin"

        print("names cleaned and replaced:", self.cookie_names)

        #  Get images
        self.cookie_image_urls = []
        for i in range(1, num_cookies + 1):
            for img_type in self.image_file_types:
                if img_type in content_str_broken_for_name[i]:
                    print()
                    print("image cookie's name:", self.cookie_image_names[i - 1].replace(' ', ''))
                    img_url = content_str_broken_for_name[i].split(img_type)[0].split('https://')[-1]
                    print("image url:", img_url)
                    img_url = 'https://' + img_url + img_type
                    # print(img_url)
                    if self.cookie_image_names[i - 1].replace(' ', '') in img_url:  # Check if the first 5 chars of the cookie name match in the image
                        # print("Added")
                        self.cookie_image_urls.append(img_url)
                    continue


    def save_cookies(self, dir):
        print("urls:", self.cookie_image_urls)
        for i in range(len(self.cookie_names)):
            img_type = self.cookie_image_urls[i][-4:]
            with open(dir + '/' + self.cookie_names[i].replace(' ', '') + img_type, 'wb') as file:
                file.write(requests.get(self.cookie_image_urls[i]).content)




if __name__ == "__main__":
    crumbl = Crumbl()
    crumbl.get_cookies()
    print()
    print("Post get_cookies()")
    print(crumbl.cookie_names)
    print(crumbl.cookie_image_urls)
    crumbl.save_cookies('resources/crumbl/')





