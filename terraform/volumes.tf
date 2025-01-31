# EBS Volume
resource "aws_ebs_volume" "additional_storage" {
  count             = length(aws_instance.app_instance)
  availability_zone = aws_instance.app_instance[count.index].availability_zone
  size              = 50 # Size in GB
  type              = "gp2"

  tags = {
    Name = "htx-additional-storage-${count.index + 1}"
  }
}

# Attach the EBS Volume to the EC2 Instance
resource "aws_volume_attachment" "attach_additional_storage" {
  count       = length(aws_instance.app_instance)
  device_name = "/dev/sdf"
  volume_id   = aws_ebs_volume.additional_storage[count.index].id
  instance_id = aws_instance.app_instance[count.index].id
}