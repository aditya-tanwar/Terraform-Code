

# when creating the modules we dont have to define the provider block 
# which provider to use 

# provider "aws" {
#   region = "us-east-1"
# }


# Terraform block to have terraform related configs 

terraform {
  required_version = ">= 1.0" # this is terraform version 

  required_providers { # this sets the configuration for the provide to use 
    aws = {
      source  = "hashicorp/aws"
    }
  }

# this is the default backend type here we can make adjustments to the path where to store the tfstate file 
  # backend "local" {
  #   path = "terraform.tfstate"
    
  # }
}

