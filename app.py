from flask import Flask, render_template, request, jsonify
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)

# Airport code mapping (common airports)
AIRPORT_CODES = {
    "DELHI": "DEL",
    "NEW DELHI": "DEL",
    "MUMBAI": "BOM",
    "BANGALORE": "BLR",
    "BENGALURU": "BLR",
    "CHENNAI": "MAA",
    "KOLKATA": "CCU",
    "HYDERABAD": "HYD",
    "AHMEDABAD": "AMD",
    "PUNE": "PNQ",
    "GOA": "GOI",
    "JAIPUR": "JAI",
    "LUCKNOW": "LKO",
    "KOCHI": "COK",
    "COCHIN": "COK",
    "THIRUVANANTHAPURAM": "TRV",
    "TRIVANDRUM": "TRV",
    "GUWAHATI": "GAU",
    "BHUBANESWAR": "BBI",
    "PATNA": "PAT",
    "CHANDIGARH": "IXC",
    "NAGPUR": "NAG",
    "COIMBATORE": "CJB",
    "INDORE": "IDR",
    "KOZHIKODE": "CCJ",
    "CALICUT": "CCJ",
    "VISAKHAPATNAM": "VTZ",
    "VIZAG": "VTZ",
    "VARANASI": "VNS",
    "SRINAGAR": "SXR",
    "SILIGURI": "IXB",
    "BAGDOGRA": "IXB",
    "MANGALORE": "IXE",
    "MANGALURU": "IXE",
    "TIRUCHIRAPPALLI": "TRZ",
    "TRICHY": "TRZ",
    "MADURAI": "IXM",
    "AGARTALA": "IXA",
    "IMPHAL": "IMF",
    "RANCHI": "IXR",
    "RAIPUR": "RPR",
    "UDAIPUR": "UDR",
    "DEHRADUN": "DED",
    "JODHPUR": "JDH",
    "JAMMU": "IXJ",
    "PORT BLAIR": "IXZ",
    "LAKSHADWEEP": "AGX",
    "AGATTI": "AGX",
    "DIBRUGARH": "DIB",
    "DIMAPUR": "DMU",
    "JORHAT": "JRH",
    "SILCHAR": "IXS",
    "AIZAWL": "AJL",
    "SHILLONG": "SHL",
    "TEZPUR": "TEZ",
    "LILABARI": "IXI",
    "NORTH LAKHIMPUR": "IXI",
    "BHUJ": "BHJ",
    "JAMNAGAR": "JGA",
    "KANDLA": "IXY",
    "PORBANDAR": "PBD",
    "RAJKOT": "RAJ",
    "SURAT": "STV",
    "VADODARA": "BDQ",
    "BARODA": "BDQ",
    "AURANGABAD": "IXU",
    "BHOPAL": "BHO",
    "DURGAPUR": "RDP",
    "GAYA": "GAY",
    "HUBLI": "HBX",
    "JABALPUR": "JLR",
    "KHAJURAHO": "HJR",
    "LEH": "IXL",
    "LUDHIANA": "LUH",
    "TIRUPATI": "TIR",
    "VIJAYAWADA": "VGA",
    "VISHAKHAPATNAM": "VTZ",
    "NEW YORK": "JFK",
    "LONDON": "LHR",
    "PARIS": "CDG",
    "TOKYO": "HND",
    "SYDNEY": "SYD",
    "DUBAI": "DXB",
    "SINGAPORE": "SIN",
    "BANGKOK": "BKK",
    "HONG KONG": "HKG",
    "TORONTO": "YYZ",
    "LOS ANGELES": "LAX",
    "CHICAGO": "ORD",
    "SAN FRANCISCO": "SFO",
    "MIAMI": "MIA",
    "SEATTLE": "SEA",
    "BOSTON": "BOS",
    "WASHINGTON": "IAD",
    "ATLANTA": "ATL",
    "DALLAS": "DFW",
    "HOUSTON": "IAH",
    "DENVER": "DEN",
    "LAS VEGAS": "LAS",
    "ORLANDO": "MCO",
    "PHILADELPHIA": "PHL",
    "PHOENIX": "PHX",
    "BEIJING": "PEK",
    "SHANGHAI": "PVG",
    "GUANGZHOU": "CAN",
    "SEOUL": "ICN",
    "KUALA LUMPUR": "KUL",
    "JAKARTA": "CGK",
    "MANILA": "MNL",
    "TAIPEI": "TPE",
    "HANOI": "HAN",
    "HO CHI MINH CITY": "SGN",
    "SAIGON": "SGN",
    "MELBOURNE": "MEL",
    "BRISBANE": "BNE",
    "PERTH": "PER",
    "AUCKLAND": "AKL",
    "CHRISTCHURCH": "CHC",
    "WELLINGTON": "WLG",
    "AMSTERDAM": "AMS",
    "FRANKFURT": "FRA",
    "MUNICH": "MUC",
    "ZURICH": "ZRH",
    "GENEVA": "GVA",
    "ROME": "FCO",
    "MILAN": "MXP",
    "MADRID": "MAD",
    "BARCELONA": "BCN",
    "LISBON": "LIS",
    "ATHENS": "ATH",
    "ISTANBUL": "IST",
    "MOSCOW": "SVO",
    "ST PETERSBURG": "LED",
    "VIENNA": "VIE",
    "BRUSSELS": "BRU",
    "COPENHAGEN": "CPH",
    "OSLO": "OSL",
    "STOCKHOLM": "ARN",
    "HELSINKI": "HEL",
    "BERLIN": "BER",
    "HAMBURG": "HAM",
    "DUBLIN": "DUB",
    "MANCHESTER": "MAN",
    "EDINBURGH": "EDI",
    "GLASGOW": "GLA",
    "JOHANNESBURG": "JNB",
    "CAPE TOWN": "CPT",
    "DURBAN": "DUR",
    "NAIROBI": "NBO",
    "CAIRO": "CAI",
    "CASABLANCA": "CMN",
    "LAGOS": "LOS",
    "ADDIS ABABA": "ADD",
    "MAURITIUS": "MRU",
    "SEYCHELLES": "SEZ",
    "TEL AVIV": "TLV",
    "DOHA": "DOH",
    "ABU DHABI": "AUH",
    "RIYADH": "RUH",
    "JEDDAH": "JED",
    "MUSCAT": "MCT",
    "BAHRAIN": "BAH",
    "KUWAIT": "KWI",
    "TEHRAN": "IKA",
    "BEIRUT": "BEY",
    "AMMAN": "AMM",
    "COLOMBO": "CMB",
    "MALE": "MLE",
    "KATHMANDU": "KTM",
    "DHAKA": "DAC",
    "KARACHI": "KHI",
    "LAHORE": "LHE",
    "ISLAMABAD": "ISB",
    "KABUL": "KBL",
    "TASHKENT": "TAS",
    "ALMATY": "ALA",
    "BISHKEK": "FRU",
    "DUSHANBE": "DYU",
    "ASHGABAT": "ASB",
    "BAKU": "GYD",
    "TBILISI": "TBS",
    "YEREVAN": "EVN",
    "ASTANA": "NQZ",
    "NUR-SULTAN": "NQZ",
    "ULAANBAATAR": "ULN",
    "PYONGYANG": "FNJ",
    "VLADIVOSTOK": "VVO",
    "KHABAROVSK": "KHV",
    "IRKUTSK": "IKT",
    "NOVOSIBIRSK": "OVB",
    "YEKATERINBURG": "SVX",
    "KAZAN": "KZN",
    "SAMARA": "KUF",
    "ROSTOV-ON-DON": "ROV",
    "SOCHI": "AER",
    "MINSK": "MSQ",
    "KIEV": "KBP",
    "KYIV": "KBP",
    "ODESSA": "ODS",
    "LVIV": "LWO",
    "CHISINAU": "KIV",
    "BUCHAREST": "OTP",
    "SOFIA": "SOF",
    "BELGRADE": "BEG",
    "ZAGREB": "ZAG",
    "SARAJEVO": "SJJ",
    "SKOPJE": "SKP",
    "TIRANA": "TIA",
    "PODGORICA": "TGD",
    "PRISTINA": "PRN",
    "BUDAPEST": "BUD",
    "PRAGUE": "PRG",
    "WARSAW": "WAW",
    "KRAKOW": "KRK",
    "GDANSK": "GDN",
    "WROCLAW": "WRO",
    "VILNIUS": "VNO",
    "RIGA": "RIX",
    "TALLINN": "TLL",
    "REYKJAVIK": "KEF",
    "NUUK": "GOH",
    "HAVANA": "HAV",
    "MEXICO CITY": "MEX",
    "CANCUN": "CUN",
    "GUADALAJARA": "GDL",
    "MONTERREY": "MTY",
    "PANAMA CITY": "PTY",
    "SAN JOSE": "SJO",
    "MANAGUA": "MGA",
    "TEGUCIGALPA": "TGU",
    "SAN SALVADOR": "SAL",
    "GUATEMALA CITY": "GUA",
    "BELIZE CITY": "BZE",
    "NASSAU": "NAS",
    "KINGSTON": "KIN",
    "MONTEGO BAY": "MBJ",
    "PORT-AU-PRINCE": "PAP",
    "SANTO DOMINGO": "SDQ",
    "SAN JUAN": "SJU",
    "ST. MAARTEN": "SXM",
    "BRIDGETOWN": "BGI",
    "PORT OF SPAIN": "POS",
    "GEORGETOWN": "GEO",
    "PARAMARIBO": "PBM",
    "CAYENNE": "CAY",
    "BOGOTA": "BOG",
    "MEDELLIN": "MDE",
    "CALI": "CLO",
    "CARTAGENA": "CTG",
    "QUITO": "UIO",
    "GUAYAQUIL": "GYE",
    "LIMA": "LIM",
    "CUSCO": "CUZ",
    "LA PAZ": "LPB",
    "SANTA CRUZ": "VVI",
    "SANTIAGO": "SCL",
    "BUENOS AIRES": "EZE",
    "CORDOBA": "COR",
    "MENDOZA": "MDZ",
    "MONTEVIDEO": "MVD",
    "ASUNCION": "ASU",
    "RIO DE JANEIRO": "GIG",
    "SAO PAULO": "GRU",
    "BRASILIA": "BSB",
    "SALVADOR": "SSA",
    "RECIFE": "REC",
    "FORTALEZA": "FOR",
    "MANAUS": "MAO",
    "BELEM": "BEL",
    "CURITIBA": "CWB",
    "PORTO ALEGRE": "POA",
    "FLORIANOPOLIS": "FLN",
    "CARACAS": "CCS",
    "MARACAIBO": "MAR",
    "VALENCIA": "VLN",
    "BARQUISIMETO": "BRM",
    "MARACAY": "MYC",
    "PORLAMAR": "PMV",
    "BARCELONA": "BLA",
    "MATURIN": "MUN",
    "PUERTO ORDAZ": "PZO",
    "SAN CRISTOBAL": "SCI",
    "MERIDA": "MID",
    "BARRANQUILLA": "BAQ",
    "SANTA MARTA": "SMR",
    "PEREIRA": "PEI",
    "BUCARAMANGA": "BGA",
    "CUCUTA": "CUC",
    "LETICIA": "LET",
    "SAN ANDRES": "ADZ",
    "PASTO": "PSO",
    "MANIZALES": "MZL",
    "NEIVA": "NVA",
    "VALLEDUPAR": "VUP",
    "MONTERIA": "MTR",
    "ARMENIA": "AXM",
    "POPAYAN": "PPN",
    "RIOHACHA": "RCH",
    "ARAUCA": "AUC",
    "QUIBDO": "UIB",
    "TUMACO": "TCO",
    "VILLAVICENCIO": "VVC",
    "YOPAL": "EYP",
    "PUERTO ASIS": "PUU",
    "IPIALES": "IPI",
    "BARRANCABERMEJA": "EJA",
    "COROZAL": "CZU",
    "FLORENCIA": "FLA",
    "GUAPI": "GPI",
    "MITU": "MVP",
    "NUQUI": "NQU",
    "PROVIDENCIA": "PVA",
    "PUERTO CARRENO": "PCR",
    "PUERTO INIRIDA": "PDA",
    "SAN JOSE DEL GUAVIARE": "SJE",
    "SARAVENA": "RVE",
    "TAME": "TME",
    "TRINIDAD": "TDA",
    "TULUA": "ULQ",
    "TURBO": "TRB",
    "APARTADO": "APO",
    "BAHIA SOLANO": "BSC",
    "BUENAVENTURA": "BUN",
    "CAPURGANA": "CPB",
    "CARTAGO": "CRC",
    "CAUCASIA": "CAQ",
    "CHIGORODO": "IRO",
    "CONDOTO": "COG",
    "EL BAGRE": "EBG",
    "EL BANCO": "ELB",
    "EL CHARCO": "ECO",
    "EL YOPAL": "EYP",
    "GUAVIARE": "SJE",
    "INIRIDA": "PDA",
    "JURADO": "JUO",
    "LA CHORRERA": "LCR",
    "LA MACARENA": "LMC",
    "LA PEDRERA": "LPD",
    "LETICIA": "LET",
    "LOPEZ DE MICAY": "LMI",
    "MAGANGUE": "MGN",
    "MEDELLIN": "MDE",
    "MITU": "MVP",
    "MOCOA": "MQU",
    "MONTERIA": "MTR",
    "NECOCLI": "NCI",
    "NUQUI": "NQU",
    "OCANA": "OCV",
    "ORITO": "ORO",
    "PASTO": "PSO",
    "PEREIRA": "PEI",
    "PITALITO": "PTX",
    "POPAYAN": "PPN",
    "PROVIDENCIA": "PVA",
    "PUERTO ASIS": "PUU",
    "PUERTO BERRIO": "PBE",
    "PUERTO CARRENO": "PCR",
    "PUERTO GAITAN": "PGT",
    "PUERTO INIRIDA": "PDA",
    "PUERTO LEGUIZAMO": "LGZ",
    "PUERTO NARE": "NAR",
    "PUERTO RICO": "PCC",
    "QUIBDO": "UIB",
    "RIOHACHA": "RCH",
    "SAN ANDRES": "ADZ",
    "SAN JOSE DEL GUAVIARE": "SJE",
    "SAN VICENTE DEL CAGUAN": "SVI",
    "SANTA MARTA": "SMR",
    "SANTIAGO": "SNT",
    "SARAVENA": "RVE",
    "TAME": "TME",
    "TOLU": "TLU",
    "TUMACO": "TCO",
    "TURBO": "TRB",
    "VALLEDUPAR": "VUP",
    "VILLAGARZON": "VGZ",
    "VILLAVICENCIO": "VVC",
    "YOPAL": "EYP"
}

# Function to extract airport code from location string
def get_airport_code(location_string):
    # Check if the location string contains an airport code in parentheses
    if "(" in location_string and ")" in location_string:
        # Extract the code from the format "City, Country (CODE)"
        code = location_string.split("(")[1].split(")")[0].strip()
        return code
    
    # If no code in parentheses, try to match the city name to our dictionary
    location_upper = location_string.upper()
    for city, code in AIRPORT_CODES.items():
        if city in location_upper:
            return code
    
    # If no match found, return a default code
    print(f"Could not find airport code for: {location_string}")
    return "DEL"  # Default to Delhi as fallback

# Get flight data from SerpAPI
def get_flight_data(source_code, destination_code, date):
    import requests
    from datetime import datetime
    
    # Format the date as YYYY-MM-DD
    try:
        # Try to parse the date if it's in a readable format
        date_obj = datetime.strptime(date.split(" to ")[0], "%B %d, %Y")
        formatted_date = date_obj.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Date parsing error: {e}")
        # Default to a future date if parsing fails
        formatted_date = "2025-05-14"
    
    # Get airport codes from the location names
    source_airport = get_airport_code(source_code)
    destination_airport = get_airport_code(destination_code)
    
    print(f"Looking for flights from {source_airport} to {destination_airport} on {formatted_date}")
    
    # Make the actual API call
    api_key = "306055ebacd927c7d7dc5dd0d213a831d12ea6a27f72f69eadd0763101a52113"  # This should be in an environment variable in production
    url = f"https://serpapi.com/search.json?engine=google_flights&type=2&departure_id={source_airport}&arrival_id={destination_airport}&outbound_date={formatted_date}&currency=INR&hl=en&api_key={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            # Add booking URLs and convert prices to INR if needed
            for flight_group in data.get("best_flights", []):
                # Create a booking URL using Google Flights
                booking_url = f"https://www.google.com/travel/flights?hl=en&gl=in&curr=INR&tfs=CBwQAhoeEgoyMDI1LTA1LTE0agcIARID{source_airport}cgcIARID{destination_airport}"
                flight_group["booking_url"] = booking_url
                
                # If price is in USD, convert to INR (approximately)
                if "price" in flight_group and isinstance(flight_group["price"], (int, float)):
                    # Add currency symbol to indicate INR
                    flight_group["currency"] = "INR"
            
            return data
        else:
            print(f"API error: {response.status_code} - {response.text}")
            # Fall back to the mock data if API call fails
            return get_mock_flight_data(source_airport, destination_airport)
    except Exception as e:
        print(f"Error calling SerpAPI: {e}")
        # Fall back to the mock data if API call fails
        return get_mock_flight_data(source_airport, destination_airport)

# Get mock flight data as a fallback
def get_mock_flight_data(source_airport, destination_airport):
    json_file_path = os.path.join(os.path.dirname(__file__), 'jsonFile.json')
    
    try:
        # Check if the file exists
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                
                # Add booking URLs to the flight data and convert prices to INR
                for flight_group in data.get("best_flights", []):
                    # Create a booking URL using Google Flights
                    booking_url = f"https://www.google.com/travel/flights?hl=en&gl=in&curr=INR&tfs=CBwQAhoeEgoyMDI1LTA1LTE0agcIARID{source_airport}cgcIARID{destination_airport}"
                    flight_group["booking_url"] = booking_url
                    
                    # Convert USD to INR (approximate conversion rate)
                    if "price" in flight_group and isinstance(flight_group["price"], (int, float)):
                        flight_group["price"] = int(flight_group["price"] * 83)  # Approximate USD to INR conversion
                        flight_group["currency"] = "INR"
                
                return data
        else:
            # Return a simple mock response if file doesn't exist
            return {
                "best_flights": [
                    {
                        "flights": [
                            {
                                "departure_airport": {
                                    "name": f"{source_airport} International Airport",
                                    "id": source_airport,
                                    "time": "2025-05-14 08:20"
                                },
                                "arrival_airport": {
                                    "name": f"{destination_airport} International Airport",
                                    "id": destination_airport,
                                    "time": "2025-05-14 12:55"
                                },
                                "duration": 215,
                                "airline": "Mock Airline",
                                "flight_number": "MA 123"
                            }
                        ],
                        "price": 52124,  # 628 USD converted to INR
                        "currency": "INR",
                        "total_duration": 1708,
                        "booking_url": f"https://www.google.com/travel/flights?hl=en&gl=in&curr=INR&tfs=CBwQAhoeEgoyMDI1LTA1LTE0agcIARID{source_airport}cgcIARID{destination_airport}"
                    }
                ]
            }
    except Exception as e:
        print(f"Error loading mock flight data: {e}")
        return {}

# Get airport code from location name
def get_airport_code(location):
    # Clean up the location string
    location = location.strip().upper()
    
    # Check if the location is in our mapping
    if location in AIRPORT_CODES:
        return AIRPORT_CODES[location]
    
    # Check if any part of the location matches our mapping
    parts = location.split(',')
    for part in parts:
        part = part.strip()
        if part in AIRPORT_CODES:
            return AIRPORT_CODES[part]
    
    # If we can't find a match, just use the first 3 characters
    # This is a fallback and not ideal
    return location[:3]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    # Get user inputs
    data = request.json
    source = data.get('source')
    destination = data.get('destination')
    dates = data.get('dates')
    budget = data.get('budget')
    travelers = data.get('travelers')
    interests = data.get('interests')
    # Always set these to false/true to remove AI flight recommendations and always show real-time data
    include_flights = False
    include_transportation = True
    
    # Validate inputs
    if not all([source, destination, dates, budget, travelers]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Create prompt for Gemini
    prompt = f"""
    Create a detailed travel plan with the following information:
    - Source: {source}
    - Destination: {destination}
    - Travel Dates: {dates}
    - Budget: {budget} (in Indian Rupees)
    - Number of Travelers: {travelers}
    {f'- Interests: {interests}' if interests else ''}
    
    Format your response in Markdown with proper headings, lists, and emphasis.
    All costs should be in Indian Rupees (₹).
    
    Please include:
    
    # Travel Plan: {source} to {destination}
    
    ## Overview
    *A comprehensive overview of the destination with key highlights, best time to visit, and cultural significance*
    
    ## Accommodation Options
    *Suggest 3-4 accommodation options within the budget with brief descriptions, amenities, and approximate costs in Indian Rupees*
    
    ## Day-by-Day Itinerary
    *Detailed daily plan with activities, attractions, and estimated costs. If the user hasn't specified interests, include a variety of popular attractions, cultural experiences, and hidden gems*
    
    ## Local Cuisine
    *Recommendations for must-try local foods, popular restaurants, and approximate meal costs*
    
    ## Travel Tips
    *Practical advice specific to the destination including local transportation, safety tips, cultural etiquette, and language basics*
    
    ## Packing Suggestions
    *What to bring based on the destination, weather during the travel dates, and planned activities*
    
    ## Budget Breakdown
    *Detailed estimated costs in Indian Rupees (₹) for accommodation, food, activities, local transportation, and miscellaneous expenses*
    """
    
    # Add flight details request if selected
    if include_flights:
        prompt += f"""
    ## Flight Options
    *Recommended airlines, flight durations, estimated costs, and booking tips*
    """
    
    try:
        # Generate content using Gemini 1.5 Flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        # Process and return the response
        travel_plan = response.text
        
        # Always get flight data
        flight_data = get_flight_data(source, destination, dates)
        
        return jsonify({
            "travel_plan": travel_plan,
            "flight_data": flight_data
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a separate endpoint for getting just flight data
@app.route('/get_flights', methods=['POST'])
def get_flights():
    try:
        data = request.json
        source = data.get('source')
        destination = data.get('destination')
        dates = data.get('dates')
        
        if not all([source, destination, dates]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Get flight data
        flight_data = get_flight_data(source, destination, dates)
        
        return jsonify(flight_data)
    except Exception as e:
        print(f"Error getting flight data: {e}")
        return jsonify({"error": str(e)}), 500

# Location autocomplete endpoint removed

if __name__ == '__main__':
    app.run(debug=True)