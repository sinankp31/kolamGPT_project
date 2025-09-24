# KolamGPT 🎨

An AI-powered web application for analyzing and understanding traditional South Indian kolam patterns. Upload kolam images and get detailed AI analysis including pattern recognition, cultural insights, and digital recreations.

![KolamGPT](https://img.shields.io/badge/KolamGPT-AI%20Analysis-blue?style=for-the-badge&logo=ai)
![React](https://img.shields.io/badge/React-19.1.1-61DAFB?style=flat&logo=react)
![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=flat&logo=flask)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?style=flat&logo=google)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=flat&logo=opencv)

## 🌟 Features

### 🔍 **AI-Powered Analysis**
- **Pattern Recognition**: Advanced computer vision algorithms detect dots, lines, and geometric patterns
- **Cultural Insights**: AI analysis provides cultural context and regional significance
- **Mathematical Analysis**: Graph theory analysis of pattern connectivity and symmetry

### 🎨 **Digital Recreation**
- **AI-Generated Images**: Create digital versions of traditional kolam patterns
- **Pattern Classification**: Identify pattern types, symmetry, and complexity levels
- **Regional Identification**: Determine likely region of origin (Tamil Nadu, Karnataka, etc.)

### 🌐 **Modern Web Interface**
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Processing**: Instant analysis with loading indicators
- **Interactive UI**: Intuitive drag-and-drop image upload

### 📧 **Contact Integration**
- **Email Notifications**: Contact form with automated email responses
- **Professional Support**: Direct communication channel for users

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Google Gemini API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kolamgpt.git
   cd kolamgpt
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your Google Gemini API key and email settings
   python run.py
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

4. **Access the Application**
   - Frontend: http://localhost:5175
   - Backend API: http://localhost:5001

## 📁 Project Structure

```
kolamgpt/
├── backend/                 # Flask API Backend
│   ├── app/
│   │   ├── __init__.py     # Flask app factory
│   │   ├── api/
│   │   │   ├── routes.py   # API endpoints
│   │   │   └── __init__.py
│   │   ├── kolam_analysis/ # Core analysis modules
│   │   │   ├── analyzer.py     # Pattern analysis logic
│   │   │   ├── image_processor.py # Image processing
│   │   │   └── models.py       # Data models
│   │   ├── services/       # External service integrations
│   │   │   ├── ai_service.py   # Google Gemini integration
│   │   │   └── vision_service.py # Computer vision pipeline
│   │   └── utils/          # Utility functions
│   │       └── image_utils.py
│   ├── config.py           # Configuration settings
│   ├── requirements.txt    # Python dependencies
│   └── run.py             # Application entry point
├── frontend/               # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── landing/    # Landing page components
│   │   │   ├── common/     # Shared components
│   │   │   └── AnalysisDisplay/ # Analysis results
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service functions
│   │   ├── hooks/          # Custom React hooks
│   │   └── utils/          # Frontend utilities
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your_secret_key_here
GOOGLE_API_KEY=your_google_gemini_api_key
GEMINI_MODEL_NAME=gemini-1.5-flash

# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com
CONTACT_RECIPIENT=your_email@gmail.com
```

### API Keys

1. **Google Gemini API**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Email Service**: Configure Gmail app password for contact form functionality

## 🎯 Usage

### Analyzing a Kolam

1. **Upload Image**: Drag and drop or click to upload a kolam image
2. **AI Processing**: The system analyzes the pattern using computer vision
3. **View Results**: Get detailed analysis including:
   - Pattern structure and complexity
   - Symmetry analysis
   - Cultural significance
   - Digital recreation
   - Regional classification

### API Endpoints

- `POST /api/analyze_kolam` - Analyze kolam image
- `POST /api/chat` - Text-based kolam queries
- `POST /api/contact` - Send contact form messages

## 🛠️ Technology Stack

### Backend
- **Flask**: Lightweight Python web framework
- **OpenCV**: Computer vision and image processing
- **Google Gemini**: AI analysis and generation
- **NetworkX**: Graph theory for pattern analysis
- **Pillow**: Image manipulation
- **Flask-Mail**: Email functionality

### Frontend
- **React 19**: Modern JavaScript library
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Lucide React**: Beautiful icons

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Traditional Kolam Artists**: For preserving this beautiful cultural art form
- **South Indian Culture**: For the rich heritage that inspires this project
- **Open Source Community**: For the amazing tools and libraries

## 📞 Contact

- **Project Lead**: Team Horizon
- **Email**: muhammedsinankp31@gmail.com
- **GitHub**: https://github.com/sinankp31/kolamGPT_project

---

**Made with ❤️ for the preservation and celebration of traditional South Indian art**
