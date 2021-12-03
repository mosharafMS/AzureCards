import json
import requests
from bs4  import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
import argparse
import shutil 
import os

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
        product['product_cost_link']=get_price_link(product['product_link'])
        # add a new field for cost
        product['product_cost']=''
        # add a new field for cost rating
        product['product_cost_rating']=''
        # add a new field for security
        product['product_security']=''
        # add a new field for security rating
        product['product_security_rating']=''
        # add a new field for performance
        product['product_performance']=''
        # add a new field for performance rating
        product['product_performance_rating']=''
        # add a new field for complexity
        product['product_complexity']=''
        # add a new field for complexity rating
        product['product_complexity_rating']=''
        # add a new field for accessibility
        product['product_accessibility']=''
        # add a new field for accessibility rating
        product['product_accessibility_rating']=''
        # add a new field for support
        product['product_support']=''
        # add a new field for support rating
        product['product_support_rating']=''
        # add a new field for interoperability
        product['product_interoperability']=''
        # add a new field for interoperability rating
        product['product_interoperability_rating']=''
        # add a new field for data handling
        product['product_data_handling']=''
        
       
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
    with open('resources/card_template.md', 'r') as f:
        template = f.read()
    
    # copy the rating pictures from resources folder to the img folder
    for file in os.listdir('resources/'):
        if file.endswith(".png") or file.endswith(".svg"):
            shutil.copy('resources/'+file, 'img/')
    
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
            markdown=markdown.replace('{{product_cost_link}}',product['product_cost_link'])
            markdown=markdown.replace('{{product_cost}}',product['product_cost'])
            markdown=markdown.replace('{{product_cost_rating_pic}}','../img/'+product['product_cost_rating']+'star.png')
            markdown=markdown.replace('{{product_security}}',product['product_security'])
            markdown=markdown.replace('{{product_security_rating_pic}}','../img/'+product['product_security_rating']+'star.png')
            markdown=markdown.replace('{{product_performance}}',product['product_performance'])
            markdown=markdown.replace('{{product_performance_rating_pic}}','../img/'+product['product_performance_rating']+'star.png')
            markdown=markdown.replace('{{product_complexity}}',product['product_complexity'])
            markdown=markdown.replace('{{product_complexity_rating_pic}}','../img/'+product['product_complexity_rating']+'star.png')
            markdown=markdown.replace('{{product_accessibility}}',product['product_accessibility'])
            markdown=markdown.replace('{{product_accessibility_rating_pic}}','../img/'+product['product_accessibility_rating']+'star.png')
            markdown=markdown.replace('{{product_support}}',product['product_support'])
            markdown=markdown.replace('{{product_support_rating_pic}}','../img/'+product['product_support_rating']+'star.png')
            markdown=markdown.replace('{{product_interoperability}}',product['product_interoperability'])
            markdown=markdown.replace('{{product_interoperability_rating_pic}}','../img/'+product['product_interoperability_rating']+'star.png')
            markdown=markdown.replace('{{product_data_handling}}',product['product_data_handling'])
            #save the markdown in a new file
            Path("output/").mkdir(parents=True, exist_ok=True)
            with open('output/'+product['product_name']+'.md', 'w',encoding='utf-8') as f:
                f.write(markdown)
            #update the template with the product info

# check the passed arguments    
def check_arguments():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',description='From the list of Azure services groups listed in the services.json file, generate a json file per service group and from it generate a markdown file with each product card')
    parser.add_argument('-jo', '--json-only', help='Generate only the json file', required=False, action='store_true')
    parser.add_argument('-mo', '--markdown-only', help='Generate only the markdown file', required=False, action='store_true')
    args = parser.parse_args()
    return args
  
    


# main function. the entry point of the program
def main():
    #check passed arguments
    args=check_arguments()
    
    service_group = get_servicesGroup('services.json')
    #loop through all the service_group
    for service in service_group:
        if not args.markdown_only:
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
        if not args.json_only:
            #generate the markdown file
            generate_markdown_file(service)
        

if __name__ == '__main__':
    main()
    

