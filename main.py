from bs4 import BeautifulSoup
import requests
import json

try:
    source = requests.get('https://www.filmweb.pl/ranking/film')
    source.raise_for_status()

    json_data = []
    soup = BeautifulSoup(source.text, 'html.parser')
    movies = (soup.find('div', class_="page__container rankingTypeSection__container")
              .find_all('div', class_="rankingType"))
    for movie in movies:
        title_pl = movie.find('h2', class_="rankingType__title").find('a').text
        org_data = movie.find('p', class_="rankingType__originalTitle").text.split(' ')
        url = movie.find('h2', class_="rankingType__title").find('a')
        rate = movie.find('span', class_='rankingType__rate--value').text.replace(",", ".")
        votes = movie.find('span', itemprop='ratingCount')['content']
        place = movie.find('span', itemprop='position').text
        img_src = movie.find('img')['src']
        find_genres = movie.find('div', class_='rankingType__genres').find_all('a')

        genre = ''
        year = 0
        org_title = ''

        # Getting description from url
        desc_src = requests.get(f"https://www.filmweb.pl{url['href']}")
        desc_src.raise_for_status()
        desc_soup = BeautifulSoup(desc_src.text, 'html.parser')
        description = (desc_soup.find('span', itemprop="description")).text
        # end

        #Getting genres
        for genres in find_genres:
            new_genre = genres.find('span').text
            genre += new_genre + ' '

        # Extracting year and original title from p tag
        for dat in org_data:
            if dat == org_data[-1]:
                year = dat
            else:
                org_title += dat + ' '

        # Creating json representation object

        json_obj = {
            "place": place,
            "title": title_pl,
            "original_title": org_title.strip(),
            "year": int(year),
            "description": description,
            "genre": genre.strip().replace(" ", " / "),
            "rate": float(rate),
            "total_votes": int(votes),
            "image": img_src
        }
        json_data.append(json_obj)

    with open("data.json", "w", encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=2)


except Exception as e:
    print(e)