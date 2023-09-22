variable "instance_name" {
  type        = string
  description = "Name for the Google Compute instance"
}
variable "instance_zone" {
  type        = string
  description = "Zone for the Google Compute instance"
  default     = "us-west1-c"
  validation {
    condition = contains(["us-west1-b", "us-west1-c"], var.instance_zone)
    error_message = "Allowed zones : us-west1-b, us-west1-c"
  }
}
variable "instance_type" {
  type        = string
  description = "Disk type of the Google Compute instance"
  default     = "e2-medium"
}