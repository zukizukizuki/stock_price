terraform {
  required_version = "~> 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.35.0"
    }

    null = {
      source  = "hashicorp/null"
      version = "~> 3.1.1"
    }
  }
}
