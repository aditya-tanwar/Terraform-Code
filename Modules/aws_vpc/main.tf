resource "aws_vpc" "aws_vpc_example" {
    cidr_block = var.vpc_cidr
    tags = {
        Name = var.vpc_name
    }
  
}