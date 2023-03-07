from bs4 import BeautifulSoup
import urllib.request
import os

url =  'https://leagueoflegends.fandom.com/wiki/League_of_Legends:_Wild_Rift'
save_path = 'hero'
save_image_path = os.path.join(save_path, 'hero_avatar')
if not os.path.exists(save_path):
   os.makedirs(save_path)
if not os.path.exists(save_image_path):
   os.makedirs(save_image_path)
save_txt_path = os.path.join(save_path, 'hero_avatar.txt')

page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

hero_list_soup = soup.find('div', class_='columntemplate').find_all('img')
hero_list = []
hero_list_name = []
for hero in hero_list_soup:
    name = hero.get('alt').replace(' ', '_').replace('\'', '')
    link = hero.get('data-src')
    hero_list.append({'name': name, 'link': link[:link.index('png')+3]})
    hero_list_name.append(name)
# print(hero_list)
# print(len(hero_list))

with open('test_data/hero_names.txt') as f:
    hero_list_test = [line.strip() for line in f]


count = 0
with open (save_txt_path, 'w') as f:
    for hero in hero_list:
        print(hero['name'])
        if hero['name'] in hero_list_test:
            image_path = os.path.join(save_image_path, hero['name'] + ".jpg")
            urllib.request.urlretrieve(hero['link'], image_path)
            f.write(image_path + '\t' + hero['name']+'\n')
            count += 1

print(hero_list_test)
if count != len(hero_list_test):
    print('Not Enough {} compare with {}'.format(count, len(hero_list_test)))

for i in hero_list_test:
    if i not in hero_list_name:
        print(i)
    

