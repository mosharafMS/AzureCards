# <img src ="../img/Data Factory.svg" width=100 /> Data Factory                 



## Description										
Azure Data Factory is Azure's cloud ETL service for scale-out serverless data integration and data transformation.  It offers a code-free UI for intuitive authoring and single-pane-of-glass monitoring and management. You can also lift and shift existing SSIS packages to Azure and run them with full compatibility in ADF. SSIS Integration Runtime offers a fully managed service, so you don't have to worry about infrastructure management.



## Documentation
https://docs.microsoft.com/en-us/azure/data-factory/


## Security		<img src="../img/4star.png" width=100 />  
Data Factory is available in the Canadian regions. 
 Azure Data Factory including Azure Integration Runtime and Self-hosted Integration Runtime does not store any temporary data, cache data or logs except for linked service credentials for cloud data stores, which are encrypted by using certificates. 
 Data encryption in transit: If the cloud data store supports HTTPS or TLS, all data transfers between data movement services in Data Factory and a cloud data store are via secure channel HTTPS or TLS.
 https://docs.microsoft.com/en-us/azure/data-factory/data-movement-security-considerations


## Performance		<img src="../img/4star.png" width=100 />
Azure Data Factory and Synapse pipelines offer a serverless architecture that allows parallelism at different levels.
 This architecture allows you to develop pipelines that maximize data movement throughput for your environment.
 A single copy activity can take advantage of scalable compute resources.When using Azure integration runtime (IR), you can specify up to 256 data integration units (DIUs) for each copy activity, in a serverless manner.
 Data Factory Data Flow utilize spark clusters for fast in-memory data engineering. You can scale up the performance based on the cluster size

	
## Complexity		<img src="../img/5star.png" width=100 />
Azure Data Factory is low-code/no-code data engineering thus the learning curve is not steep. It's a cloud service so the setup and maintainance is very easy.


## Accessibility		<img src="../img/3star.png" width=100 />
Azure Portal and Data Factory portal sport accessible interface


## Supportability		<img src="../img/5star.png" width=100 />
Official Microsoft support and community support is available


## Interoperability		<img src="../img/5star.png" width=100 />
Data Factory is very well integrated with the rest of the Azure data services


## Data handling
Data Factory doesn't save data in it, it just move data between data sources


## Cost 		<img src="../img/5star.png" width=100 />
Data Factory cost is per use. Pricing for Data Pipeline is calculated based on: 
 - Pipeline orchestration and execution 
 - Data flow execution and debugging 
 - Number of Data Factory operations such as create pipelines and pipeline monitoring
https://azure.microsoft.com/en-us/pricing/details/data-factory




