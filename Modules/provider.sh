#!/bin/bash


cat << EOF >> provider.tf
provider "aws" {
    region = "us-west-2"
    alias = "acc-${account_id}"
    assume_role {
        role_arn = "arn:aws:iam::${account_id}:role/${role_name}"
        external_id = "${role_name}"
    }
}

EOF