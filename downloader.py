import requests
import json
from requests.exceptions import HTTPError

class Downloader():
	"""Methods to help download remote resources.
	"""

	@classmethod
	def download_to(self, url, dest_path, headers={}, params={}):
		"""Downloads content and stores it in specified destination path.
		"""

		try:
			response = requests.get(url, headers=headers, params=params)

			with open(dest_path, "w+") as dest_file:
				dest_file.write(response.text)

		except HTTPError as http_error:
			print(http_error)

		except Exception as e:
			print(e)
