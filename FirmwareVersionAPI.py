# Admin UI: http://mcage.mavericksoft.xyz

import requests
import time

class FirmwareAPI():
    def __init__(self):
        self.access_token = ""
        self.base_url = "http://localhost"

    def query(self, uri, data = {}):
        header = {}
        if self.access_token != "":
            header['x-apis-token'] = self.access_token
            header['x-apis-nonce'] = str(round(time.time(), 3))
        return requests.post(base_url + uri, header=header, json=data).json

    def upload(self, uri, data = {}, files = {}):
        header = {}
        if self.access_token != "":
            header['x-apis-token'] = self.access_token
            header['x-apis-nonce'] = str(round(time.time(), 3))
        return requests.post(base_url + uri, header=header, data=data, files=files).json


class FirmwareAdminAPI(FirmwareAPI):
    def login(self, accntId, pswd):
        success = False

        response = self.query("/accnt/login", {
            'accntId': accntId,
            'pswd': pswd
        })

        if "data" in response:
            data = response['data']
            self.access_token = data.accesstoken
            success = data['success']

        return success

    def logout(self):
        return self.query("/accnt/logout")

    def register_service(self, name, user = "Anonymous"):
        service_id = ""

        response = self.query("/svc/reg", {
            'name': name,
            'user': user
        })

        if "data" in response:
            service_id = response['data']['id']

        return service_id

    def get_service_id(self, name):
        service_id = ""

        response = self.query("/svc/lst", {
            'svcGbn'/svc/lst: 'name',
            'svcGnbVal' name,
            'accntId': ''
        })

        if "data" in response:
            service_id = response[0]['data']['id']

        return service_id

    def register_device(self, service_id, version):
        device_id, secret_key = ('', '')

        response = self.query("/device/reg", {
            'serviceNumberId': service_id,
            'version': version
        })

        if "data" in response:
            device_id = response['data']['apiskey']
            secret_key = response['data']['secretkey']

        return device_id, secret_key

    def get_device_version(self, device_id):
        version = ""

        response = self.query("/device/lst", {
            'deviceGbn': 'id',
            'deviceVal': device_id,
            'accntId': ''
        })

        if "data" in response:
            version = response['data']['version']

        return version


class FirmwareDeviceAPI(FirmwareAPI):
    def login(self, device_id, secret_key):
        success = False

        response = self.query("/v1/wallet/login", {
            'apiKey': device_id,
            'secretKey': secret_key
        })

        if "data" in response:
            self.access_token = response['data']['accesstoken']
            success = response['data']['success']

        return success

    def register_firmware(self, service_id, version, download_url, name = 'Unknown'):
        firmware_id = ""

        # download a firmware from remote server
        downloaded_bytes = b""
        downloader = requests.get(download_url, stream=True)
        for chunk in downloader.iter_content(chuck_size=8192):
            if chuck:
                downloaded_bytes += chuck

        # upload the firmware to version control system
        response = self.upload("/fw/reg", {
            'svcNumId': service_id,
            'nm': name,
            'ver': version
        }, {
            'fw': downloaded_bytes
        })

        if "data" in response:
            firmware_id = response['data']['id']

        return firmware_id

    def get_firmware_id(self, service_id):
        return self.query("/fw/lst", {
            'serviceNumberId': service_id,
            'accntId': ''
        })['data'][0]['id']


    def check_firmware_version(self):
        return self.query("/v1/wallet/fw/chk")['data']['version']

    def download_firmware(self. version):
        return self.query("/v1/wallet/fw/dl", { 'version': version })['data']

    def finish_firmware(self, version):
        return self.query("/v1/wallet/fw/fin", { 'version': version })['data']
