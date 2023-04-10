# **ProjectApiTwitter**
**Novidades:**
- Seção explicando como criar uma pipeline no Jenkins para realizar o deploy do código.
- Remoção dos métodos "film_to_actors_gz_to_json()" e "get_film_to_actors_list()", responsáveis por criar arquivos json com os dados filtrados e recuperá-los, respectivamente. Sendo atríbuidas ao método "top_ten_acts_to_json()" as funções dos métodos removidos.
## **Funcionamento da aplicação:**
Ao se executar o script “main.py” o programa verifica a data da última execução que está armazenada no arquivo “last_update.json”, se for diferente da data atual, o algoritmo irá fazer o download da base dados e executar a sequência de métodos que irão fazer a extração e filtragem dos dados necessários para a execução do programa, armazenado tudo em arquivos “.json” e apagando a base de dados original (não mais necessária para a execução do código).

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

	> ~~**film_to_actors_gz_to_json():** este método pega a relação filme-profissionais mas já filtrando pelo ano de lançamento. Escrevendo em um arquivo json.~~

	> ~~**get_film_to_actors_list()**: análogo ao “def get_title_basic_dic()”, porém retorna uma lista realacionando os códigos de filmes a códigos de atores que estavam armazendos no json.~~
	
	> **top_ten_acts_to_json()**: esse método conta o número de filmes que o ator ou atriz participou e armazena os dez que mais fizeram filmes em um arquivo json. O contagem é feita diretamente do dataset original agora, deixando a execução mais lenta, porém com um menor uso de memória.
	
	 >**def get_top_ten_acts_list():** método análogo ao “def get_film_to_actors_list()”,porém retorna uma lista com os nomes dos top 10 atores e a quantidade de filmes que estavam armazenados no json. E, no final, apaga os dados originais da base de dados.

   - O script “JSONManipulator.py” contém os métodos responsáveis por escrever e ler dados em arquivos “.json”. É um script auxiliar.
 
- Por fim, temos o arquivo **“access.properties”** que tem as keys e tokens escritos no padrão “chave:valor”, o **“last_update.json”** (com a última data de execução), **"pythonversion.txt"** que tem a versão do python em que a aplicação foi desenvolvida, **"requirements.txt"** arquivo com os dados das dependências utilizadas no projeto para a instalação  e o script **“main.py”**.
## **Tarefas agendadas, EC2 e S3:**
Depois de descarregar os arquivos do projeto na raíz da máquina EC2, será necessário instalar as depedências do código com:

    pip3 install -r requirements.txt
    
Um arquivo script.cron deverá ser criado com o conteúdo:
		
	*/10 * * * * python3 main.py
	* * * * * aws s3 sync ./data/twitterdata/ link_bucket_
		
Lembrando que os cinco asteriscos da primeira linha definem o periodo em que o código será executado, recomendo checar documentação ou utilizar a ferramenta *[Crontab Guru](https://crontab.guru/)*. No exemplo acima o código main.py será executado a cada 10 min e a sincronização com o bucket ocorrerá a cada 1 min.
Por fim, para setar as tarefas basta utilizar o comando:

	crontab script.cron 

## **Tarefas agendadas Windows, PowerShell, S3:**
Depois de descarregar os arquivos do projeto na raíz da máquina EC2, será necessário instalar as depedências do código com:

    pip install -r requirements.txt
    
Um arquivo *run_app.ps1* deverá ser criado na pasta do projeto com este conteúdo:
		
		set-Location "caminho_até_raiz_do_projeto"  
		python main.py
Um arquivo *sinc_s3.ps1* também deverá ser criado na pasta do projeto com este conteúdo:

		aws s3 sync "path_até_raiz_do projeto\data\twitterdata" s3://pasta_no_bucket

Com isso temos os dois scripts PowerShell que serão exeutados no agendamento de tarefas.

O próximo passo é abrir o "Agendador de tarefas" do Windows. E para cada um dos scripts criar uma nova tarefa. 
- Para o **run_app.ps1**:
> Criar uma nova tarefa rápida, escolher o nome da tarefa, escolher o período e  escolher como ação "iniciar um programa". Na etapa "iniciar um programa", no campo "programa/script" você deverá escrever "PowerShell" e apenas no compo "Adicione argumentos" que você colocará o caminho até onde o seu arquivo "run_app.ps1" está.
 - Para o **sinc_s3.ps1**:
> Deverá segui os mesmo passos anteriores, apenas trocando path no campo "Adicione argumentos", pondo o caminhi até onde o "sinc_s3.ps1" está.

**É importante que a tarefa criada para o "sinc_s3.ps1" tenha uma frequência diferente da "run_app.ps1", pois a tarefa criada para o app tem a execução demorada, isso deve ser levado em consideração!**
## **Pipeline Jenkins para deploy do código:**
Após instalar o Jenkins e instalar o git na máquina a ser usada, deverá ser criada uma nova tarefa do tipo pipeline.
Antes, é necessário que seja criada uma pasta em um bucket no S3, onde você deverá criar um arquivo "last_update.json". É nessa pasta que será atualizada a data da ultima execução do código.
Então, na parte do script da pipeline deverá ser escrito o seguinte: 

    pipeline {  
		agent any  
		stages {  
			stage('Git Checkout'){  
				steps {  
					git credentialsId: '-your-credentialsId-', branch: 'main', url: '-your-github-project-url-'  
				}  
			}  
			stage('Download access.prop, last_update and Install Requirements'){  
				steps {  
					sh 'rm last_update.json'  
					sh 'aws s3 sync -path-to-last-update-in-S3-bucket .'  
					sh 'pip install -r requirements.txt'  
				}  
			}  
			stage('App Run') {  
				steps {  
					sh 'python3 main.py'  
				}  
			}  
			stage('Saving last_update') {  
				steps {  
					sh 'aws s3 cp last_update.json -path-to-last-update-in-S3-/last_update.json'  
				}  
			}  
		}  
	}
 
