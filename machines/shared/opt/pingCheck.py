#!/usr/bin/env python3
import os
import re
from argparse import ArgumentParser
import sys

parser = ArgumentParser(description="Pings machines to see if they're up")

parser.add_argument('-l','--log',help="log to /hostlab/.logs",action="store_true")
parser.add_argument('-v','--verbose',help="display extra info in terminal",action="store_true")
# args=parser.parse_args()
args=parser.parse_args()

global logOutput, printOutput,debug
logOutput=0
printOutput=1
debug=0

if args.log:
	logOutput=1

if args.verbose:
	debug=1


class Colour:
	FAIL = "\033[91m"
	SUCCESS = "\033[92m"
	TITLE = "\033[33m"
	WARN = "\033[7m"
	END="\033[0m"


os.chdir("/hostlab")

if logOutput==1:
	try:
		os.mkdir(".logs")
		if debug==1:
			print("Making .logs directory in /hostlab")
	except FileExistsError as e:
		if debug==1:
			print("Directory exists")
			print(f"{e}")
			print("Skipping directory creation")
		None

if debug==1:
	print("Getting machine directories in /hostlab")
dirs = os.listdir()
if debug==1:
	print(dirs)
	print("Getting startup files for each directory found")


startups = []
for i in dirs:
	startupCheck = i[-8:]
	if startupCheck == ".startup":
		startups.append(i)
if debug==1:
	print(f"Startups: {startups}")

def addToDict(machine,address):
	if machine in hostnameDict.keys():
		hostnameDict[machine].append(address)
	else:
		hostnameDict[machine] = []
		hostnameDict[machine].append(address)

def removeDuplicates():
	for i in hostnameDict.keys():
		hostnameDict[i] = list(set(hostnameDict[i]))



global hostnameDict
hostnameDict = {}

interfacePattern = r"address\s+([\d\.]+)"
iproute2Pattern = r"ip addr add\s+([\d\.]+)"
ifconfigPattern = r"ifconfig eth\d+ ([\d\.]+)"

if debug==1:
	print("Parsing .startup files")
for machine in startups:
	with open(machine) as startup:
		machineName = machine.replace(".startup","")
		if debug==1:
			print(f"Parsing: {machineName}")
		content=startup.read()
		if "ifup" in content:
			if debug==1:
				print(f"\tReading /etc/network/interfaces")
			#print(machine)
			dirName = machine.replace(".startup","")
			with open(f"{dirName}/etc/network/interfaces") as interfaceFile:
				config = interfaceFile.read()
				matches = re.findall(interfacePattern,config)
				#print(matches)
				for address in matches:
					if debug==1:
						print(f"\tAddress: {address}")
					addToDict(machine,address) 
		if debug==1:
			print(f"\tParsing iproute2 ip addresses")
		if "ip addr add" in content:
			matches=re.findall(iproute2Pattern,content)
			#print(matches)
			#ips.append(matches)
			for address in list(matches):
				if debug==1:
					print(f"\tAddress: {address}")
				addToDict(machine,address)
		if debug==1:
			print(f"\tParsing ifconfig ip addresses")
		if "ifconfig" in content:
			matches = re.findall(ifconfigPattern,content)
			#print(matches)
			for address in list(matches):
				if debug==1:
					print(f"Address: {address}")
				addToDict(machine,address)

removeDuplicates()
hostname = os.popen("hostname").read().strip()
bridges = []
# if debug==1:
# 	print(f"HostnameDict: {hostnameDict}")
# 	print(f"Hostname: {hostname}")

if debug==1:
	print(f"Opening {hostname}.log in /hostlab/.logs/")
if logOutput==1:
	log=open(f"./.logs/{hostname}.log","w")

if debug==1:
	print("Listing Machines")
title=f"{Colour.TITLE}---- Machines ----{Colour.END}"
if printOutput==1:
	print(title)
if logOutput==1:
	log.write(f"{title}\n")

startups=sorted(startups)

for machine in startups:
	machineName = machine.replace(".startup","")
	if machineName=="shared":
		continue
	if logOutput==1:
		log.write(f"{machineName}\n")
	
	if printOutput==1:
		print(machineName)

title=f"\n\n\n{Colour.TITLE}---- Pings ----{Colour.END}"

if logOutput==1:
	log.write(f"{title}\n")
if printOutput==1:
	print(title)


for machine in sorted(hostnameDict.keys()):
	machineName = machine.replace(".startup","")

	for ip in hostnameDict[machine]:
		if debug==1:
			print(f"Machine: {machine}\nIP: {ip}\n")
	#print(i)	
	#print(hostnameDict[i])
		if ip == "0.0.0.0":
			bridges.append(machine)
			
		else:
			if debug==1:
				print(f"pinging {ip}")
			response = os.system(f"ping -c 1 {ip} >/dev/null 2>&1")
			if response == 0:
				success=f"{machineName}:{Colour.SUCCESS} Connected{Colour.END} @ {ip}"
				if printOutput==1:
					print(success)
				if logOutput==1:
					log.write(f"{success}\n")
			else:
				error=f"{machineName}: {Colour.FAIL}Error{Colour.END} @ {ip}"
				if printOutput==1:
					print(error)
				if logOutput==1:
					log.write(f"{error}\n")
				if debug==1:
					print(f"Ping to {ip} failed")

if debug==1:
	print("Listing bridges")
bridges=list(set(bridges))
bridges=sorted(bridges)
if len(bridges)>0:
	title=f"\n\n\n{Colour.TITLE}---- Bridges ----{Colour.END}"
	if logOutput==1:
		log.write(f"{title}\n")
	if printOutput==1:
		print(f"{title}")
	for machine in bridges:
		machineName = machine.replace(".startup","")
		if logOutput==1:
			log.write(f"{machineName}\n")
		if printOutput==1:
			print(machineName)

for machine in bridges:
	machineName=machine.replace(".startup","")
	if machineName==hostname:
		print(f"{Colour.WARN}Current machine is bridge so might not ping all machines{Colour.END}")





