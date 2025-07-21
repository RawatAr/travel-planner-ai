# AI Travel Planner

An intelligent travel planning application that uses Google's Gemini AI to generate personalized travel plans and flight information.
Live Link: https://travel-planner-m739ct27t-rawatars-projects.vercel.app/

## Features

- AI-powered travel planning
- Flight information lookup
- Airport code mapping
- Interactive web interface
- Real-time travel recommendations

## Prerequisites

- Python 3.8 or higher
- Google Cloud account with Gemini API access
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/travel-planner-ai.git
cd travel-planner-ai
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Enter your travel details and let the AI generate your personalized travel plan!

## Project Structure

```
travel-planner-ai/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in git)
├── .gitignore        # Git ignore file
├── templates/        # HTML templates
│   └── index.html    # Main web interface
└── static/          # Static files (CSS, JS, images)
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for powering the travel recommendations
- Flask for the web framework
- All contributors who have helped shape this project
