terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.57.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_servicequotas_service_quota" "vpc_per_region_quota" {
        quota_code = "L-F678F1CE"
        service_code = "vpc"
        value = "2" # This value should always be higher than the default value
}
