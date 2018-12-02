#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import boto3
import pprint
import cgi


def _exit(msg=None):
	if msg!=None: print(msg)
	print("\n\n")


print("Content-type:application/json\n\n")

data = cgi.FieldStorage()

print(data)


if (not os.path.exists("aws.json")):
	print(json.dumps({"error": "aws.json does not exist"}))
	sys.exit(0)

with open("aws.json") as conf_infile:
	conf = json.load(conf_infile)
	
session = boto3.Session(aws_access_key_id=conf["access_key_id"],aws_secret_access_key=conf["access_secret_key"],region_name=conf["region"])
ec2 = session.client("ec2")
res = session.resource("ec2")


if "action" in data:
	if data["action"]=="start":
		if not "id" in data:
			print(json.dumps({"error": "No ID specified"}))
			_exit()


dis = ec2.describe_instances()

instances = []

for i in dis["Reservations"][0]["Instances"]:
	vol = res.Volume(i["BlockDeviceMappings"][0]["Ebs"]["VolumeId"])
	current = {
		"id": i["InstanceId"],
		"architecture": i["Architecture"],
		"type": i["InstanceType"],
		"last-launch": "{0:%d}.{0:%m}.{0:%Y} at {0:%H}:{0:%M}".format(i["LaunchTime"]),
		"private-ip": i["PrivateIpAddress"],
		"state": i["State"]["Name"],
		"tags": i["Tags"],
		"size": vol.size
	}
	instances.append(current)



print(json.dumps(instances))



_exit()
