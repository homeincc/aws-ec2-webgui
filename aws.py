#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import boto3
import pprint
import cgi


def _err(msg):
	print(json.dumps({"error": msg}))

def _exit(msg=None):
	if msg!=None: print(msg)
	print("\n\n")
	sys.exit(0)


print("Content-type:application/json\n\n")

query = {}

qs = os.environ.get("QUERY_STRING","")

if qs!="":
	for arg in qs.split("&"):
		name, val = arg.split("=")
		query[name] = val


if (not os.path.exists("aws.json")):
	_err("aws.json does not exist")
	_exit()

with open("aws.json") as conf_infile:
	conf = json.load(conf_infile)
	
session = boto3.Session(aws_access_key_id=conf["access_key_id"],aws_secret_access_key=conf["access_secret_key"],region_name=conf["region"])
ec2 = session.client("ec2")
res = session.resource("ec2")


if "action" in query:
	if query["action"]=="start":
		if not "id" in query:
			_err("No ID specified")
			_exit()
		ec2.start_instances(InstanceIds=[query["id"]])
		print(json.dumps({"status": "ok"}))
		_exit()
	elif query["action"]=="stop":
		if not "id" in query:
			_err("No ID specified")
			_exit()
		ec2.stop_instances(InstanceIds=[query["id"]])
		print(json.dumps({"status": "ok"}))
		_exit()

dis = ec2.describe_instances()

instances = []

for r in range(len(dis["Reservations"])):
	for i in dis["Reservations"][r]["Instances"]:
		vol = res.Volume(i["BlockDeviceMappings"][0]["Ebs"]["VolumeId"])
		current = {
			"id": i["InstanceId"],
			"architecture": i["Architecture"],
			"type": i["InstanceType"],
			"last-launch": "{0:%d}.{0:%m}.{0:%Y} at {0:%H}:{0:%M}".format(i["LaunchTime"]),
			"private-ip": i["PrivateIpAddress"],
			"state": i["State"]["Name"],
			"tags": i["Tags"],
			"size": vol.size,
			"args": query
		}
		instances.append(current)



print(json.dumps(instances))



_exit()
