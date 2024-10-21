import httpx
from typing import List, Dict, Any
import csv
import os
import aiofiles


class WifeedAPIClient:
	BASE_URL = "https://wifeed.vn/api/du-lieu-gia-eod/full"

	def __init__(self, api_key: str):
		self.api_key = api_key

	async def fetch_stock_data(
			self, code: str, from_date: str, to_date: str
	) -> List[Dict[str, Any]]:
		"""Fetch stock price data from the API."""
		params = {
			"apikey": self.api_key,
			"code": code,
			"from-date": from_date,
			"to-date": to_date,
		}

		async with httpx.AsyncClient() as client:
			response = await client.get(self.BASE_URL, params=params)

			# Raise an error for bad responses
			response.raise_for_status()

			return response.json()

	async def turn_it_into_csv(self, data: List[Dict[str, Any]], filename: str) -> str:
		os.makedirs('data', exist_ok=True)
		file_path = os.path.join('data', f"{filename}.csv")

		async with aiofiles.open(file_path, mode='w', newline='') as csvfile:
			if data:
				fieldnames = data[0].keys()
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

				await csvfile.write(','.join(fieldnames) + '\n')

				for row in data:
					await csvfile.write(','.join(str(row[field]) for field in fieldnames) + '\n')

		return file_path



async def main():
	api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTg5LCJlbWFpbCI6Imh1YW5uZ3V5ZW5AdWVoLmVkdS52biIsIm5hbWUiOiJOZ3V54buFbiBI4buvdSBIdcOibiIsInBob25lIjoiKzg0OTk5OTk5OTk5IiwiY29tcGFueSI6IlByb21ldGUiLCJyb2xlIjoidXNlciIsImlhdCI6MTcwMjQ4NDAxNn0._5-kIGOHqD7H0UQTTAspn1o1ndL4CMDau21nS9jBwcY"
	client = WifeedAPIClient(api_key)

	code = "FPT"
	from_date = "2000-01-01"
	to_date = "2024-01-01"

	try:
		data = await client.fetch_stock_data(code, from_date, to_date)
		csv_file = await client.turn_it_into_csv(data, f"{code}")
		print(f"Data saved to {csv_file}")
	except Exception as e:
		print(f"An error occurred: {e}")

if __name__ == "__main__":
	import asyncio
	asyncio.run(main())

