export AWS_DEFAULT_REGION="your-region"
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
cd /tmp/tweets-project-source/
sh aws_credencials_var_env.sh
pip3 install -r requirements.txt
python3 main.py