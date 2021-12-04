# Generate markdown cards for Azure Products



 This tool scrap the Azure documentation site, and generate markdown cards with info about different Azure serviecs.



## Usage:

Fill the services.json with the categories of Azure services under serviceGroups with the links. Here's the sample 



```json
{
    "servicesGroups": [
        {
            "name": "Analytics ",
            "docLink": "https://docs.microsoft.com/en-us/azure/?product=analytics"
        },
        {
            "name": "Databases ",
            "docLink": "https://docs.microsoft.com/en-us/azure/?product=databases"
        },
        {
            "name": "AI + Machine Learning ",
            "docLink": "https://docs.microsoft.com/en-us/azure/?product=ai-machine-learning"
        },
        {
            "name": "Compute ",
            "docLink": "https://docs.microsoft.com/en-us/azure/?product=compute"
        },
        {
            "name": "Storage ",
            "docLink": "https://docs.microsoft.com/en-us/azure/?product=storage"
        },
        {
            "name": "Security ",
            "docLink": "https://docs.microsoft.com/en-us/azure/?product=security"
        },
        {
            "name": "Identity ",
            "docLink": "https://docs.microsoft.com/en-us/azure/?product=identity"
        }

    ]
}
```



> *Note:*
>
> *There's a trailing space at the end of each category as it's in the HTML. Keep it as is.*



### Execution:

This is a Python 3 script. The script does two tasks 

1) Generate json files containing info about the services and fill some of the fields from the docs 
2) Generate markdown files out of the json with the markdown template `/resources/card_template.md` 

Running the script without any parameters does both steps. 

If you want to generate the json only so you can update it before generating the markdown, use -jo parameter 

```bash
python main.py -jo
```

After generating the json file, fill the extra empty fields then generate the markdown using -mo parameter r

```bash
python main.py -mo
```

