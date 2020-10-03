#!/mnt/c/Users/aduma/Desktop/personal_work/car_scraper/venv/bin/python3
# INSTALLED MODULES
import requests
import bs4 as bs4

# STL MODULES
import re, sys, getopt, json, copy

# MADE MODULES


def get_wanted_urls(searches, reg):
    new_list = []
    for url in searches:
        if re.search(reg, url):
            new_list.append(url)
    return new_list


def handle_args(argv):
    given_car_brand = ""
    given_price = ""

    ### ARG HANDLING ###
    try:
        opts, args = getopt.getopt(argv, "hb:p:", ["brand=","price="])
    except getopt.GetoptError:
        print("main.py err in args.")

    for opt, arg in opts:
        if opt == '-h':
            print("USAGE: ./main.py -b <brand_name> -p <price>")
            sys.exit()
        elif opt in ("-b", "--brand"):
            given_car_brand = arg
        elif opt in ("-p", "--price"):
            given_price = arg
    ### ARG HANDLING ###

    return given_price, given_car_brand


def get_raw_cars(soup, required_price):
    soup_result = soup.findAll("div", {"class": ["listing-data", "maincolor", "price"]})
    link_list = []
    title_list = []
    price_list = []
    for res in soup_result:
        try:
            link_list.append(res.find('a', href=True)['href'])
            title_list.append(res.find('a', href=True).text.strip())
            price_list.append(res.find('strong').text.strip())
        except TypeError:
            continue
    result = {}
    for item, link, price in zip(title_list, link_list, price_list):
        price = price.replace("EUR","")
        price = "".join(price.split())
        price = int(price)
        if price > required_price:
            continue
        temp_dict = {"title" : item, "url" : link, "price" : price}
        result["car_details:" + item] = temp_dict

    return result

def main(argv):
    """ ENTRYPOINT """

    SEARCH_URLS = [
    "https://www.publi24.ro/anunturi/auto-moto/masini-second-hand/bmw/",
    "https://www.olx.ro/auto-masini-moto-ambarcatiuni/autoturisme/timisoara/q-bmw/"
    ]

    given_tuple = handle_args(argv)
    given_price = given_tuple[0]
    given_car_brand = given_tuple[1]
    wanted_reg = given_car_brand
    wanted_price = int(given_price)

    url_l = get_wanted_urls(SEARCH_URLS, wanted_reg)

    # for url in url_l:
    # page_content = requests.get(str(url))
    page_content = requests.get(str("https://www.publi24.ro/anunturi/auto-moto/masini-second-hand/bmw/"))
    soup = bs4.BeautifulSoup(page_content.text, 'html.parser')
    requested_cars = get_raw_cars(soup, wanted_price)

    with open("output.json", "w") as file:
        json.dump(requested_cars, file)


if __name__ == "__main__":
    main(sys.argv[1:])