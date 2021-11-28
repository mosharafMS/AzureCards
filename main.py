import json
import requests
from bs4  import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path

#Get the list of servicesGroup from the json file
def get_servicesGroup(json_file):
    service_group = []
    with open(json_file, 'r') as f:
        data = json.load(f)
        for service in data['servicesGroups']:
            service_group.append(service)
    return service_group


# download the link of a serviceGroup
def download_link(service_group):
    service_group_link=service_group['docLink']
    # download the link
    html=requests.get(service_group_link).text
    return html

#parse the html to get the product cards
def get_product_cards(html,service_group):
    soup = BeautifulSoup(html, 'html.parser')
    #get all the product cards using div with data-categories attribute equal to service_group name
    div_product_service_group = soup.find_all('div', attrs={'data-categories': service_group['name']})
    return div_product_service_group


#parse product_cards to get name, description, link and picture
def get_product_info(product_cards):
    product_info=[]
    for product in product_cards:
        #get the name of the product
        product_name=product.find('h3').text
        #get the description of the product
        product_description=product.find('p').text
        #get the link of the product
        product_link=product.find('a')['href']
        #get the picture of the product
        product_picture=product.find('img')['src']
        product_info.append({'product_name':product_name,'product_description':product_description,'product_link':product_link,'product_picture':product_picture})
    return product_info


#save the products_info in a json file
def save_products_info(products_info,doc_link,service_group):
    # update the product_link to full link,update the description and download the images
    for product in products_info:
        #if the product_link has / in it, take the last part
        if '/' in product['product_link'] and not product['product_link'].endswith('/'):
            product['product_link']=urljoin(doc_link, product['product_link'].split('/')[-1])
        else:
            product['product_link']=urljoin(doc_link,product['product_link'])
        # get the full description from the meta summary of the product_link and update it if not empty
        full_description=get_full_description(product['product_link'])
        if(full_description!=''):
            product['product_description']=full_description
        #download the image

        #check if the product_picture is a valid full link
        if not product['product_picture'].startswith('http'):
            product['product_picture']=urljoin('https://docs.microsoft.com/en-us/azure/', product['product_picture'])
        p_image=requests.get(product['product_picture'])

        #save the image in the folder
        Path("img/").mkdir(parents=True, exist_ok=True)
        image_path='img/'+product['product_name']+'.svg'
        with open(image_path,'wb') as f:
            f.write(p_image.content)
        
            
        #update the product_picture to the name of the image
        product['product_picture']=image_path
        # add new field for price_link
        product['price_link']=get_price_link(product['product_link'])
        # add a new field for architectural function
        product['architectural_function']=''
        # add a new field for security
        product['security']=''
       
    #save the products_info in a json file
    Path("output/").mkdir(parents=True, exist_ok=True)    
    with open('output/'+service_group.strip()+'.json', 'w') as f:
        json.dump(products_info, f)


# get the price link from the product_link
def get_price_link(product_link):
    # remove the trailing slash from the product_link
    product_link=product_link.rstrip('/')
    #split the last part of the url
    product_name=product_link.split('/')[-1]
    price_link=urljoin('https://azure.microsoft.com/en-us/pricing/details/',product_name)
    return price_link


#get the full description from the meta summary of the product_link
def get_full_description(product_link):
    html=requests.get(product_link).text
    soup = BeautifulSoup(html, 'html.parser')
    summary_tag=soup.find('meta', attrs={'name': 'summary'})
    #check if summary_tag is not None
    if summary_tag is not None:
        description=summary_tag['content']
    else:
        description=''
    return description


# generate markdown file from json
def generate_markdown_file(service):
    #open the template file
    with open('card_template.md', 'r') as f:
        template = f.read()
    #create a new file to write the markdown
    with open('output/'+service['name'].strip()+'.json', 'r') as f:
        #loop through the products_info
        produts=json.load(f)
        for product in produts:
            #replace the template with the product_info
            markdown=template.replace('{{product_name}}',product['product_name'])
            markdown=markdown.replace('{{product_description}}',product['product_description'])
            markdown=markdown.replace('{{product_link}}',product['product_link'])
            markdown=markdown.replace('{{product_picture}}','../'+product['product_picture'])
            markdown=markdown.replace('{{price_link}}',product['price_link'])
            markdown=markdown.replace('{{architectural_function}}',product['architectural_function'])
            markdown=markdown.replace('{{security}}',product['security'])
            #save the markdown in a new file
            Path("output/").mkdir(parents=True, exist_ok=True)
            with open('output/'+product['product_name']+'.md', 'w',encoding='utf-8') as f:
                f.write(markdown)
            #update the template with the product info
        
    
    
    


# main function. the entry point of the program
def main():
    service_group = get_servicesGroup('services.json')
    #loop through all the service_group
    for service in service_group:
        #download the link of the service_group
        html=download_link(service)
        #get the product cards of the service_group
        product_cards=get_product_cards(html,service)
        #get the product info of the product cards
        products_info=get_product_info(product_cards)
        #remove the query string from the url
        doc_link = service['docLink']
        doc_link=urljoin(doc_link, urlparse(doc_link).path)  
        #save the products_info in a json file
        save_products_info(products_info,doc_link,service_group=service['name'])
        #generate the markdown file
        generate_markdown_file(service)
    

if __name__ == '__main__':
    main()
    

