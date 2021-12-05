import json
import requests
from prettytable import PrettyTable

meraki_api_key = "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"

baseUrl = "https://api.meraki.com/api/v1"

headers = {"X-Cisco-Meraki-API-Key": meraki_api_key}

print("Paso 1. Obtener los id de las organizaciones.")

urlOrgs = baseUrl + "/organizations"
respOrgs = requests.get(urlOrgs, headers=headers)

print("Request status: ", respOrgs.status_code)

response_JsonOrgs = respOrgs.json()
orgs = response_JsonOrgs

table = PrettyTable(["ID","ORGANIZACION"])

for org in orgs:
    table.add_row([org["id"], org["name"]])
print(table)

print("Paso 2. Obtener las redes de una organización a partir de la elección de un id del servicio anterior.")

idOrg = response_JsonOrgs[0]['id']
nameOrg = response_JsonOrgs[0]['name']
print("-"*100)
print("El id de la organizacion elegida es: ", idOrg, " y el nombre: ", nameOrg)
print("-"*100)

urlNetwork = urlOrgs + "/{}/networks".format(idOrg)

respNet = requests.get(urlNetwork, headers=headers)

respJsonNet = respNet.json()
networks = respJsonNet

table = PrettyTable(["NETWORK ID","ORGANIZACION ID","NAME"])

for network in networks:
    table.add_row([network["id"], network["organizationId"], network["name"]])
print(table)

print("Paso 3.Obtener los dispositivos de la red pasándole como parámetro el  networkid  obtenido en el paso anterior.")
idNetwork = respJsonNet[0]['id']
nameNetwork = respJsonNet[0]['name']

print("-"*100)
print("El networkid de la red elegida es: ", idNetwork, " y el nombre de la red: ", nameNetwork)
print("-"*100)

urlNetworkDevices = "https://api.meraki.com/api/v1/networks/{}/devices".format(idNetwork)

respNetDevices = requests.get(urlNetworkDevices, headers=headers)
respJsonNetDevices = respNetDevices.json()
devices = respJsonNetDevices

table = PrettyTable(["MODEL","FIRMWARE","MAC ADDRESS","SERIAL"])

for device in devices:
    table.add_row([device["model"], device["firmware"], device["mac"], device["serial"]])
print(table)

print("Paso 4. Obtener datos de la  red con el networkid.")

urlNetworkData = baseUrl + "/networks/{}".format(idNetwork)

respNetData = requests.get(urlNetworkData, headers=headers)
respJsonNetData = respNetData.json()
print(json.dumps(respJsonNetData, indent=4))
print("-"*100)

print("Paso 5. Obtener infomación de un dispositivo con el serial id.")
serialId = respJsonNetDevices[0]['serial']
print("-"*100)
print("El serial id es: ", serialId)
print("-"*100)

urlNetDevSerial = urlNetworkDevices + '/{}'.format(serialId)
respNetDevSerial = requests.get(urlNetDevSerial, headers=headers)
respJsonNetDevSerial = respNetDevSerial.json()
print(json.dumps(respJsonNetDevSerial, indent=4))
print("-"*100)

print("Paso 6.Obtener información del SSID para el network ID")

urlNetssid = "https://api.meraki.com/api/v1/networks/{}/wireless/ssids".format(idNetwork)
respNetssid = requests.get(urlNetssid, headers=headers)
respJsonNetssid = respNetssid.json()
print(json.dumps(respJsonNetssid, indent=4))
print("-"*100)
