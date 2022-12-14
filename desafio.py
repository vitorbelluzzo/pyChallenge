from bs4 import BeautifulSoup
import json
import requests

url = 'https://storage.googleapis.com/infosimples-public/commercia/case/product.html'   

resposta_final = {}

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

#title
resposta_final['title'] = soup.select_one('h2#product_title').get_text()


#brand
resposta_final['brand'] = soup.select_one('div.brand').get_text()

#categories
categories_list = [] 
for element in soup.select('nav.current-category > a'):
    categories_list.append(element.text)

resposta_final['categories'] = categories_list

#description
resposta_final['description'] = soup.select_one('div.product-details > p').getText().replace("\n","").strip()


#skus
sku_list = []
product = {}
sku_area = soup.select(".skus-area > div")[0]
for sku in sku_area.select(".card"):
    card_container = sku.select_one(".card-container")

    product['name'] = card_container.select_one(".sku-name").get_text().strip()

    if card_container.select_one(".sku-current-price") != None:
        product["current_price"] = float(card_container.select_one(".sku-current-price").get_text().strip().replace("$ ",""))
    else:
        product["current_price"] = None
   
    if card_container.select_one(".sku-old-price") != None:
        product["old_price"] = float(card_container.select_one(".sku-old-price").get_text().strip().replace("$ ",""))
    else:
        product["old_price"] = None

    if card_container.select_one(".card-container > i") != None:
        product["available"] = False
    else:
        product["available"] = True

    sku_list.append(product.copy())

resposta_final['skus'] = sku_list


#properties
tableProperties = soup.select('.pure-table')

propy = {}
props = []

for table in tableProperties:
    for row in table.select('tr'):
        if row.select('td') != None and row.select('td') != []:
            if row.select('td')[0]!=None:
                propy['label'] = row.select('td')[0].get_text().strip()
            if row.select('td')[1]!=None:
                propy['value'] = row.select('td')[1].get_text().strip()

            props.append(propy.copy())

            resposta_final['skus'] = sku_list
        
resposta_final['properties'] = props

#reviews
comment = {}
reviews = []

for review in soup.select('div#comments > div.review-box'):
    comment['name'] = review.select_one(".review-username").get_text().strip()
    comment['date']= review.select_one(".review-date").get_text().strip()
    comment['score']= review.select_one(".review-stars").getText().strip()
    comment['text']= review.select_one("p").getText().strip()

    reviews.append(comment.copy())

resposta_final['reviews'] =(reviews)

#reviews_average_score
review_score = soup.select_one('div#comments > h4').get_text().replace('Average score:','')
review_score = review_score.replace('/5','')

resposta_final['reviews_average_score'] = float(review_score)


#url
resposta_final['Url'] = (url)

#json
json_resposta_final = json.dumps(resposta_final)
with open('produto.json', 'w') as arquivo_json:
    arquivo_json.write(json_resposta_final)
