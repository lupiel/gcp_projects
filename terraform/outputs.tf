output "network_IP" {
  value       = google_compute_instance.vm_instance.network_interface[0].access_config[0].nat_ip
  description = "The internal ip address of the instance"
}
output "instance_link" {
  value       = google_compute_instance.vm_instance.self_link
  description = "The URI of the created resource."
}