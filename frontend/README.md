# KolamGPT Frontend

The React frontend for KolamGPT - an AI-powered web application for analyzing traditional South Indian kolam patterns.

## 🚀 Features

- **Modern React 19**: Built with the latest React features and hooks
- **Vite Build Tool**: Fast development server and optimized production builds
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **React Router**: Client-side routing for seamless navigation
- **Responsive Design**: Works perfectly on desktop and mobile devices

## 🛠️ Tech Stack

- **React 19.1.1** - Modern JavaScript library for building user interfaces
- **Vite 7.1.7** - Fast build tool and development server
- **Tailwind CSS 4.1.13** - Utility-first CSS framework
- **React Router DOM 7.9.1** - Declarative routing for React
- **Lucide React** - Beautiful & consistent icon toolkit

## 📦 Installation

```bash
npm install
```

## 🚀 Development

```bash
npm run dev
```

This will start the development server at `http://localhost:5175`

## 🏗️ Build

```bash
npm run build
```

Builds the app for production to the `dist` folder.

## 🔍 Lint

```bash
npm run lint
```

Runs ESLint to check for code quality issues.

## 👀 Preview

```bash
npm run preview
```

Preview the production build locally.

## 📁 Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # React components
│   │   ├── landing/        # Landing page components
│   │   ├── common/         # Shared components
│   │   └── AnalysisDisplay/# Analysis results display
│   ├── pages/              # Page components
│   ├── services/           # API service functions
│   ├── hooks/              # Custom React hooks
│   ├── utils/              # Utility functions
│   ├── App.jsx             # Main app component
│   ├── main.jsx            # App entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies and scripts
├── vite.config.js          # Vite configuration
├── index.html              # HTML template
└── README.md              # This file
```

## 🎨 Styling

This project uses Tailwind CSS for styling with custom configurations:

- **Montserrat Font**: Primary typography font
- **Custom Animations**: Fade-in, marquee, and spin animations
- **Kolam Patterns**: CSS background patterns inspired by traditional kolam art
- **Responsive Design**: Mobile-first approach with breakpoint utilities

## 🔧 Configuration

### Vite Configuration

The `vite.config.js` includes:
- React plugin for fast refresh
- Path aliases for clean imports
- Build optimizations

### ESLint Configuration

ESLint is configured with:
- React recommended rules
- React Hooks rules
- React Refresh plugin for Vite
- Custom rules for unused variables

## 🌐 API Integration

The frontend communicates with the Flask backend API:

- **Base URL**: `http://127.0.0.1:5001/api`
- **Endpoints**:
  - `POST /analyze_kolam` - Analyze kolam images
  - `POST /chat` - Text-based kolam queries
  - `POST /contact` - Contact form submissions

## 🤝 Contributing

1. Follow the existing code style
2. Use meaningful commit messages
3. Test your changes thoroughly
4. Update documentation as needed

## 📞 Support

For questions or issues, please contact the development team or create an issue in the main repository.