#!/usr/bin/env python

#Thoroghly destroy security groups, even ones with cyclic dependencies
# do this by first removing all rules, and then by deleting the groups

import boto3, argparse
import sys

parser = argparse.ArgumentParser(description="Delete AWS EC2 security groups")
parser.add_argument("--groupids", nargs='*', help="AWS EC2 Security Group IDs")
parser.add_argument("--groupnames", nargs='*', help="AWS EC2 Security Group Names")
args = parser.parse_args()

groupids = args.groupids
groupnames = args.groupnames

ec2 = boto3.resource('ec2')

#find id matches
sgi = ec2.security_groups.filter( Filters = [
    {'Name': 'group-id', 'Values': groupids }
] )
groups = list(sgi)

#find name matches
sgi = ec2.security_groups.filter( Filters = [
    {'Name': 'group-name', 'Values': groupnames}
] )
groups.extend(sgi)

for sg in groups:
    print "Clearing rules from group id: %s" % sg.group_id

    if len(sg.ip_permissions) > 0:
        sg.revoke_ingress(IpPermissions = sg.ip_permissions)
    if len(sg.ip_permissions_egress) > 0:
        sg.revoke_egress(IpPermissions = sg.ip_permissions_egress)

print "deleting groups"
for sg in groups:
    sg.delete()
