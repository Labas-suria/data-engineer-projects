provider "aws" {
}

resource "aws_instance" "to_app_deploy" {
    ami = var.ami_type
    instance_type = var.ec2_instance_type
    key_name = var.key_name_to_aws

    connection {
        type        = var.connection_type
        user        = var.connection_user
        private_key = file("key/felipenogueira.pem")
        host        = self.public_ip
    }

    provisioner "file" {
        source      = var.app_dir_name
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
