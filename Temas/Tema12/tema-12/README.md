# **ProjectApiTwitter**
**Novidades:**
- Adição de um método responsável por checar a estrutura dos diretórios onde os dados são armazenados, agora o programa cria as pastas caso elas não existam.
- Adição dos arquivos necessários para utilização do Terraform para criar a infraestrutura na AWS e fazer o deploy da aplicação na instância EC2 criada, isso sendo autômatizado com uma pipeline no Jenkins.
## **Funcionamento da aplicação:**
Ao se executar o script “main.py” o programa verifica a data da última execução que está armazenada no arquivo “last_update.json”, se for diferente da data atual, o algoritmo irá fazer o download da base dados e executar a sequência de métodos que irão fazer a extração e filtragem dos dados necessários para a execução do programa, armazenando os tweets e seus logs em .csv e apagando a base de dados original (não mais necessária para a execução do código).

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

## **Jenkins +GitHub+ Terraform + AWS**

Na pasta da aplicação já vem todos os arquivos necessário para o funcionamento do Terraform e do Jenkins. O main main.tf com o código para criação dad infraestrutura, o variables.tf com as variáveis utilizadas no código, o Jenkinsfile e os arquivos .sh chamados durante a execução da pipeline. 
Basicamente, após a configuração do Jenkins, será feito o download do projeto do GitHub, depois a pipeline iniciará o working directory onde estão os arquivos de configuração, o próximo passo é a criação do plano de execução, em seguida vem a etapa onde a infra é criada e a aplicação é executada e finalmente a a infra é destruída.

#### ****Jenkinsfile:****

	pipeline {
			agent any
			stages {
				stage('Terraform init') {
					steps {
						sh "./terraform_init.sh"
					}
				}
				stage('Terraform plan') {
					steps {
						sh "./terraform_plan.sh"
					}
				}
				stage('Terraform apply to deploy app in EC2') {
					steps {
						sh "./terraform_apply.sh"
					}
			}
				stage('Terraform destroy infra') {
					steps {
						sh "./terraform_destroy.sh"
					}
				}
			}
		post {
			always {
				cleanWs()
			}
		}
	}

#### **terraform_init.sh:**
	terraform init
#### **terraform_plan.sh:**
	terraform plan
#### **terraform_apply.sh:**
	terraform apply -auto-approve
#### **terraform_destroy.sh**
	terraform destroy -auto-approve

Por fim, os arquivos de configuração do Terraform (.tf):

#### variables.**tf:**

	variable "ami_type" {
		type = string
		default = "ami-09d3b3274b6c5d4aa"
	}
	variable "ec2_instance_type" {
		type = string
		default = "t2.micro"
	}
	variable "key_name_to_aws" {
		type = string
		default = "felipenogueira"
	}
	variable "connection_type" {
		type = string
		default = "ssh"
	}
	variable "connection_user" {
		type = string
		default = "ec2-user"
	}
	variable "app_dir_name" {
		type = string
		default = "tweets-project-source"
	}
	variable "app_dir_path_ec2" {
		type = string
		default = "/tmp/tweets-project-source"
	}
	variable "ec2_tag_name" {
		type = string
		default = "JT-DataEng-FelipeNogueira"
	}
	variable "ec2_tag_project" {
		type = string
		default = "ILEGRA-JT-DEVOPSCLOUD"
	}
	variable "ec2_tag_owner" {
		type = string
		default = "Felipe Nogueira"
	}
	variable "ec2_tag_economizator" {
		type = string
		default = "TRUE"
	}
	variable "ec2_tag_customerid" {
		type = string
		default = "ILEGRA-JTS"
	}
#### main.**tf:**

	provider "aws" {
	}
	resource "aws_instance" "to_app_deploy" {
		ami = var.ami_type
		instance_type = var.ec2_instance_type
		key_name = var.key_name_to_aws
		connection {
			type = var.connection_type
			user = var.connection_user
			private_key = file("key/felipenogueira.pem")
			host = self.public_ip
		}
		provisioner "file" {
			source = var.app_dir_name
			destination = var.app_dir_path_ec2
		}
		provisioner "remote-exec" {
			inline = [
				"chmod +x /tmp/tweets-project-source/init-script.sh",
				"/tmp/tweets-project-source/init-script.sh",
			]
		}
		tags = {
			Name = var.ec2_tag_name
			Project = var.ec2_tag_project
			Owner = var.ec2_tag_owner
			EC2_ECONOMIZATOR = var.ec2_tag_economizator
			CustomerID = var.ec2_tag_customerid
		}
	}
Desta forma, uma vez que seu job estja configurado no Jenkins, a pipeline subirá a infra utilizando terraform executará a aplicação na nuvem e destrirá a infra no final. 

