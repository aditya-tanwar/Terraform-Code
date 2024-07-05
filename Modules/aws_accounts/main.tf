

  


variable "role_name" {
    description = "Enter the name of the role"
    default = "s3123"
}


#-------------------------------------------------------------------
#--------- FETCHING THE LIST OF ACCOUNTS ---------------------------
#-------------------------------------------------------------------

resource "terraform_data" "accounts" {
    #triggers_replace = var.fetch_accounts == true ? 1 : 0 
    triggers_replace = [timestamp()]
    provisioner "local-exec" {
        #command = "aws organizations list-accounts | jq .Accounts[].Id > output"
        command = "cat test | jq -r .Accounts[].Id > output"
    } 
}



locals {
  account_id = file("output")
  account_list = split("\n", local.account_id)
  #accounts_unique = toset(local.account_list) # handling this in the for each loop 

}





#---------------------------------------------------
#---------- AWS PROVIDER --------------------------
#---------------------------------------------------




resource "terraform_data" "name" {
  for_each = toset(local.account_list)

  provisioner "local-exec" {
    command = "bash provider.sh"
    environment = {
      account_id = each.key
      role_name = var.role_name
    }
  }

  provisioner "local-exec" {
    when    = destroy
    on_failure = continue
    command = "rm provider.tf"
  }
}

