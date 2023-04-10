# **ProjectApiTwitter**
**Novidades:**
- Adição de mais logs no código para melhorar a vizualização do passo a passo durante a execução.
- Alteração na forma como os tweets dos atores são armazenados, ao invés de vários .json, agora a aplicação salva em tweet.csv o nome do autor e tweet recebido, e, além disso também salva tweets_log.csv o nome, tamanho do tweet e data em que coletou o tweet.
- Adição das pastas e arquivos necessários para subir a stack ELK em containers Docker.
## **Funcionamento da aplicação:**
Ao se executar o script “main.py” o programa verifica a data da última execução que está armazenada no arquivo “last_update.json”, se for diferente da data atual, o algoritmo irá fazer o download da base dados e executar a sequência de métodos que irão fazer a extração e filtragem dos dados necessários para a execução do programa, ~~armazenado tudo em arquivos “.json~~” armazenando os tweets e seus logs em .csv e apagando a base de dados original (não mais necessária para a execução do código).

A “key” e a “key_secrets” são recuperadas do “access_properties.properties” e usadas para a autenticação no objeto “API” (no projeto foi utilizada a biblioteca “tweepy”). A partir daqui o programa apenas carrega a lista com o nome dos dez autores e faz uma requisição dos 10 tweets que mencionam esses autores (desconsidera os retweets). No final, os tweets são escritos em arquivos “.json”, na forma de lista.
## **Estrutura do Projeto:**
- Na pasta “apiconsumer” fica a classe “TwitterApiConsumer.py” que é responsável pela a autenticação e realizar as “search_querys” que são buscas de tweets com parâmetros determinados (o método “get_tweets_with_search_query” da classe é responsável por isso ).

- Na pasta “data” temos duas pastas (a antiga pasta "script" foi movida para raiz e renomeada para "dataauxscripts"):

  - *A primeira*, “imdbdata”, nada mais é do que o local onde os dados referentes ao imdb serão armazenados, os dados originais (pasta “original”) e os dados extraídos e filtrados (como arquivos .json, pasta “transformed”).
  - *Na segunda pasta* dentro da pasta "data", a pasta “twitterdata”, é onde os json com os dez tweets dos atores serão armazenados.

- Na pasta "dataauxscripts"  estão todos scripts utilizados para lidar com os dados (ler, escrever, processar…). 
  - O “DownloadIMDBData.py” contém o método responsável por fazer o download dos dados brutos do site do imdb. 
  - O “IMDBDataExtractor.py” contém os métodos responsáveis por extrair os dados necessários da data base original:
	>   **title_basic_gz_to_json()**: este método pega dos dados originais apenas os títulos e códigos dos filmes dos 10 últimos anos e escreve em um arquivo json.
	
	> **get_title_basic_dic():** este método recupera os dados com os títulos dos filmes (do arquivo json previamente filtrado) e retorna um dicionário, tendo como chave o código dos filmes e, como valor, seus títulos.

	>  **search_name_basic_data(*nconst*):** este método foi criado para substituir os antigos "name_basic_gz_to_json()" e "get_name_basic_dic()" que eram responsáveis por filtrar da base de dados original uma lista com códigos de atores e os nomes correspondentes, gravá-los em arquivos .json e recuperá-los em um dicionário. Porém, eram métodos que utilizavam muita memória "desnecessariamente". O método "search_name_basic_data(nconst)", por sua vez, dado um código de ator (nconst) retorna uma lista com o código do ator, seu nome e suas profissões. Filtrando esses valores diretamente da base de dados original.
	
	> **top_ten_acts_to_json()**: esse método conta o número de filmes que o ator ou atriz participou e armazena os dez que mais fizeram filmes em um arquivo json. O contagem é feita diretamente do dataset original agora, deixando a execução mais lenta, porém com um menor uso de memória.
	
	 >**def get_top_ten_acts_list():** método análogo ao “def get_film_to_actors_list()”,porém retorna uma lista com os nomes dos top 10 atores e a quantidade de filmes que estavam armazenados no json. E, no final, apaga os dados originais da base de dados.

   - O script “JSONManipulator.py” contém os métodos responsáveis por escrever e ler dados em arquivos “.json”. É um script auxiliar.
 
- Por fim, temos o arquivo **“access.properties”** que tem as keys e tokens escritos no padrão “chave:valor”, o **“last_update.json”** (com a última data de execução), **"pythonversion.txt"** que tem a versão do python em que a aplicação foi desenvolvida, **"requirements.txt"** arquivo com os dados das dependências utilizadas no projeto para a instalação  e o script **“main.py”**.

## **ELK + Docker Compose para armazenar os logs da aplicação**

Na pasta da aplicação já vem todos os arquivos necessário para o funcionamento da stack. Desde os .yml para as configurações do Elasticsearch e Logstash em suas respctivas pastas, até o arquivo logstash.conf para a configuração da pipeline:
	
	input {  
	    file {  
	        path => "/data/twitterdata/tweets_log.csv"  
			start_position => "beginning"  
			sincedb_path => "/dev/null"  
	    }  
	}  
	filter {  
	    csv {  
	        separator => ","  
			columns => ['name', 'tweet_length', 'date']  
	        convert => {  
	            "tweet_length" => "integer"  
				"date" => "date_time"  
			}  
		}  
	}  
	output {  
	   elasticsearch{  
		    hosts => ["http://elasticsearch:9200"]  
	        index => "actors_tweets"  
	   }  
       stdout {}  
    }

Por fim, o arquivo docker-compose.yml:

	services:  
		Elasticsearch:  
			image: elasticsearch:${ELASTIC_VERSION}  
		    container_name: elasticsearch  
		    restart: always  
		    volumes:  
				- ./elasticsearch/data:/usr/share/elasticsearch/data/  
				- ./elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml:ro,z  
		    environment:  
			    ES_JAVA_OPTS: "-Xmx256m -Xms256m"  
				discovery.type: single-node  
		    ports:  
			    - '9200:9200'  
				- '9300:9300'  
			networks:  
			    - elk  
		Logstash:  
		    image: logstash:${ELASTIC_VERSION}  
		    container_name: logstash  
		    restart: always  
		    volumes:  
			    - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml:ro,Z  
			    - ./logstash/pipeline:/usr/share/logstash/pipeline:ro,Z  
				- ./data/twitterdata/:/data/twitterdata/  
    command: logstash -f /usr/share/logstash/pipeline/logstash.conf  
		    depends_on:  
			    - Elasticsearch  
		    ports:  
			    - '9600:9600'  
			environment:  
			    LS_JAVA_OPTS: "-Xmx256m -Xms256m"  
			networks:  
			    - elk  
	  Kibana:  
		    image: kibana:${ELASTIC_VERSION}  
		    container_name: kibana  
		    restart: always  
		    ports:  
			    - '5601:5601'  
			environment:  
			    - ELASTICSEARCH_URL=http://elasticsearch:9200  
		    depends_on:  
			    - Elasticsearch  
		    networks:  
			    - elk  
		volumes:  
			elastic_data: {}  
		networks:  
			  elk:

Por fim basta usar o comando:
	
	docker-compose up -d

Assim a sua stack será executada, bastando acessar http://localhost:5601/ para ter acesso ao Kibana e utilizar os logs para montar o dashboard. 

