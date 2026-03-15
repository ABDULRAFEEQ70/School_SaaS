resource "aws_instance" "app_servers" {
  count                   = var.instance_count
  ami                     = var.ami_id
  instance_type           = var.instance_type
  subnet_id               = var.subnet_ids[count.index % length(var.subnet_ids)]
  vpc_security_group_ids  = var.security_group_ids
  iam_instance_profile    = var.iam_instance_profile
  key_name               = var.key_name
  monitoring             = var.enable_monitoring
  user_data              = var.user_data

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  root_block_device {
    volume_type           = "gp3"
    volume_size           = 30
    encrypted             = true
    delete_on_termination = true
  }

  ebs_block_device {
    device_name           = "/dev/sdb"
    volume_type           = "gp3"
    volume_size           = 50
    encrypted             = true
    delete_on_termination = true
  }

  tags = merge(
    {
      Name = "${var.project_name}-${var.environment}-instance-${count.index + 1}"
    },
    var.tags
  )

  volume_tags = merge(
    {
      Name = "${var.project_name}-${var.environment}-instance-${count.index + 1}-volume"
    },
    var.tags
  )
}

resource "aws_ebs_volume" "data_volume" {
  count             = var.instance_count
  availability_zone = aws_instance.app_servers[count.index].availability_zone
  size              = 100
  type              = "gp3"
  encrypted         = true

  tags = {
    Name = "${var.project_name}-${var.environment}-data-volume-${count.index + 1}"
  }
}

resource "aws_volume_attachment" "data_volume_attachment" {
  count       = var.instance_count
  device_name = "/dev/sdc"
  volume_id   = aws_ebs_volume.data_volume[count.index].id
  instance_id = aws_instance.app_servers[count.index].id
}

resource "aws_network_interface" "secondary_nic" {
  count     = var.instance_count
  subnet_id = var.subnet_ids[(count.index + 1) % length(var.subnet_ids)]

  attachment {
    instance     = aws_instance.app_servers[count.index].id
    device_index = 1
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-nic-${count.index + 1}"
  }
}
