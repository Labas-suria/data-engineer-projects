# **Tema 10**
	
 ## ****Aplicação em container docker com Jenkins+Github**:**
 
Neste tema será demonstrada uma forma de se subir o container docker com a aplicação utilizando o jenkins+github.

### **Subir container buildando a imagem na pipeline:**

No seu repositório do projeto deverá ter todos os arquivos da sua aplicação e além deles deverá ter:

#### **Dockerfile:**

	From python:3

	ARG aws_default_region
	ARG aws_access_key_id
	ARG aws_secret_access_key

	ENV AWS_DEFAULT_REGION=$aws_default_region
	ENV AWS_ACCESS_KEY_ID=$aws_access_key_id
	ENV AWS_SECRET_ACCESS_KEY=$aws_secret_access_key

	COPY . .

	RUN pip install -r requirements.txt

	CMD python main.py

Lembrando que é importante que o AWS CLI esteja configurado, ou as variáveis de ambiente: AWS_DEFAULT_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY estejam criadas com os valores corretos para seu bucket no S3, no Jenkins. E que o repositório utilizado no Dockerfile é o repositório onde está a sua aplicação.

#### **Jenkinsfile**:

	pipeline {
		agent any
		stages {
			stage('Buildando image') {
				steps {
					sh "./buildando_imagem.sh"
				}
			}
			stage('Run container') {
				steps {
					sh "./executando_container.sh"
				}
			}
			stage('Remove container') {
				steps {
					sh  "./remover_container.sh"
				}
			}
		}
		 post { 
		 	always { 
            			cleanWs()
        		}
    		}
	}

#### **buildando_imagem.sh**:
	docker build --build-arg aws_default_region="$AWS_DEFAULT_REGION" --build-arg aws_access_key_id="$AWS_ACCESS_KEY_ID" --build-arg aws_secret_access_key="$AWS_SECRET_ACCESS_KEY" -t nome-imagem:latest .
#### **executando_container.sh**:
	docker run -i --name nome-container sua-imagem:latest
#### **remover_container**.sh:
	docker rm nome-container

Com isso, após a criação e configuração de sua tarefa, teremos nossa imagem sendo buildada durante a pipeline, a execução da nossa aplicação no container e no final a exclusão do nosso container.
