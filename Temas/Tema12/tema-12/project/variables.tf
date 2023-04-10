variable "ami_type" {
  type        = string
  default     = "ami-09d3b3274b6c5d4aa"
}
variable "ec2_instance_type" {
  type        = string
  default     = "t2.micro"
}
variable "key_name_to_aws" {
  type        = string
  default     = "felipenogueira"
}
variable "connection_type" {
  type        = string
  default     = "ssh"
}
variable "connection_user" {
  type        = string
  default     = "ec2-user"
}
variable "app_dir_name" {
  type        = string
  default     = "tweets-project-source"
}
variable "app_dir_path_ec2" {
  type        = string
  default     = "/tmp/tweets-project-source"
}
variable "ec2_tag_name" {
  type        = string
  default     = "JT-DataEng-FelipeNogueira"
}
variable "ec2_tag_project" {
  type        = string
  default     = "ILEGRA-JT-DEVOPSCLOUD"
}
variable "ec2_tag_owner" {
  type        = string
  default     = "Felipe Nogueira"
}
variable "ec2_tag_economizator" {
  type        = string
  default     = "TRUE"
}
variable "ec2_tag_customerid" {
  type        = string
  default     = "ILEGRA-JTS"
}