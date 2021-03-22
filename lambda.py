import boto3
import requests
import zipfile
import io


class LambdaManager:
    def __init__(self):
        self.client = boto3.client('lambda')
        self.lambda_functions = self._get_lambda_functions()

    def _get_lambda_functions(self):
        funcs = []
        next_marker = None

        while True:
            response = self.client.list_functions(Marker=next_marker) if next_marker else self.client.list_functions()
            for func in response['Functions']:
                funcs.append(func)
            if 'NextMarker' in  response.keys():
                next_marker = response['NextMarker']
            else:
                break
        return funcs

    def get_download_url(self, func):
        return self.client.get_function(FunctionName=func['FunctionName'])['Code']['Location']

    @staticmethod
    def download(url, file_name, path=None):
        print(file_name, url)
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(f"./lambda_functions/{file_name}" if path is None else f"{path}/{file_name}")

    @staticmethod
    # TO DO
    def upload(lambda_function, zip_file):
        pass

