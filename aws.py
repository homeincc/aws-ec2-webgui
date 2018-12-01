#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import boto3
import pprint

print("Content-type:application/json\r\n\r\n")


if (not os.path.exists("aws.json")):
	print("aws.json does not exist")
	sys.exit(0)

with open("aws.json") as conf_infile:
	conf = json.load(conf_infile)
	
session = boto3.Session(aws_access_key_id=conf["access_key_id"],aws_secret_access_key=conf["access_secret_key"],region_name=conf["region"])
ec2 = session.client("ec2")
res = session.resource("ec2")


dis = ec2.describe_instances()

instances = []

for i in dis["Reservations"][0]["Instances"]:
	vol = res.Volume(i["BlockDeviceMappings"][0]["Ebs"]["VolumeId"])
	current = {
		"architecture": i["Architecture"],
		"type": i["InstanceType"],
		"last-launch": i["LaunchTime"],
		"private-ip": i["PrivateIpAddress"],
		"state": i["State"]["Name"],
		"tags": i["Tags"],
		"size": vol.size
	}
	instances.append(current)



print(json.dumps(instances))



print("\r\n\r\n")
