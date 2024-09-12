import xml.etree.ElementTree as ET
import requests
import csv

# Ganti ini dengan URL XML kamu
url = 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaBarat.xml'

# Tambahkan header User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Ambil konten dari URL dengan header
response = requests.get(url, headers=headers)

# Cek status code dari response
if response.status_code == 200:
    xml_data = response.content
    print("Berhasil mengambil data dari URL:")
    print(xml_data.decode('utf-8'))  # Tampilkan data yang diterima dari URL
    
    # Parsing XML dari konten URL
    root = ET.fromstring(xml_data)
    
else:
    print(f"Gagal mengambil data. Status code: {response.status_code}")

# Open a CSV file to write the extracted data
with open('cuaca_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['City', 'Latitude', 'Longitude', 'Datetime (UTC)', 'Weather', 'Temperature (°C)', 'Min Temp (°C)', 
                  'Max Temp (°C)', 'Humidity (%)', 'Min Humidity (%)', 'Max Humidity (%)', 'Wind Speed (ms)', 'Wind Direction (CARD)']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Loop through the XML tree and extract relevant data
    for area in root.findall(".//area"):
        city_name = area.find('name').text
        latitude = area.get('latitude')
        longitude = area.get('longitude')

        # Fungsi untuk mengambil nilai parameter dengan aman
        def get_param_value(area, param_id):
            param = area.find(f".//parameter[@id='{param_id}']")
            if param is not None:
                value = param.find('timerange').find('value')
                if value is not None:
                    return value.text
            return None

        # Extract weather parameters
        weather = get_param_value(area, 'weather')
        temperature = get_param_value(area, 't')
        min_temp = get_param_value(area, 'tmin')
        max_temp = get_param_value(area, 'tmax')
        humidity = get_param_value(area, 'hu')
        min_humidity = get_param_value(area, 'humin')
        max_humidity = get_param_value(area, 'humax')
        wind_speed = get_param_value(area, 'ws')
        wind_direction = get_param_value(area, 'wd')

        # Extract datetime (UTC)
        for timerange in area.find(".//parameter[@id='hu']").findall('timerange'):
            time = timerange.get('datetime')

            # Write the extracted data to the CSV
            writer.writerow({
                'City': city_name,
                'Latitude': latitude,
                'Longitude': longitude,
                'Datetime (UTC)': time,
                'Weather': weather,
                'Temperature (°C)': temperature,
                'Min Temp (°C)': min_temp,
                'Max Temp (°C)': max_temp,
                'Humidity (%)': humidity,
                'Min Humidity (%)': min_humidity,
                'Max Humidity (%)': max_humidity,
                'Wind Speed (ms)': wind_speed,
                'Wind Direction (CARD)': wind_direction
            })

print("Data berhasil diambil dari URL dan disimpan ke 'cuaca_data.csv'")
