# Fay Jewelry E-commerce App

A full-stack jewelry e-commerce application built with FastAPI (backend) and Next.js (frontend) with MongoDB database.

## Features

- 🏷️ Browse jewelry by categories (Semi Mount Rings, Semi Mount Pendants, etc.)
- 📦 View detailed product information with images
- 🖼️ Image gallery for each product
- 📱 Responsive design with Tailwind CSS
- 🔄 RESTful API with FastAPI
- 🍃 MongoDB for data storage

## Project Structure

```
patrick/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main FastAPI application
│   ├── models.py           # Pydantic models
│   ├── import_data.py      # Data import script
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables
├── frontend/                # Next.js frontend
│   └── src/
│       ├── app/            # Next.js app router
│       │   ├── layout.tsx
│       │   ├── page.tsx    # Home page with categories
│       │   ├── category/[category]/page.tsx  # Category page
│       │   └── product/[id]/page.tsx         # Product detail page
│       └── components/     # React components
├── fayjewelry_products.json # Product data
└── fayjewelry_images/       # Product images
```

## Prerequisites

- Python 3.8+
- Node.js 18+
- MongoDB (local or cloud instance)

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Make sure MongoDB is running on localhost:27017
# Or update .env file with your MongoDB URL

# Import product data into MongoDB
python import_data.py

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install Node.js dependencies
npm install

# Start the Next.js development server
npm run dev
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## API Endpoints

### Categories
- `GET /categories` - Get all categories
- `GET /categories/{category}/products` - Get products by category

### Products
- `GET /products/{product_id}` - Get product details

### Images
- `GET /images/{filename}` - Serve product images

## Data Structure

The product data includes:
- **Categories**: Semi Mount Rings, Semi Mount Pendants, Semi Mount Earrings, etc.
- **Product Details**: Title, description, images, mounting info, diamond details, stone specifications
- **Images**: High-quality jewelry photos stored locally

## Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **Motor**: Async MongoDB driver
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Server Components**: React Server Components for data fetching

### Database
- **MongoDB**: NoSQL document database

## Development Notes

- The backend serves images statically from the `fayjewelry_images` directory
- CORS is configured to allow requests from the Next.js frontend
- The application uses server-side rendering for better SEO and performance
- Product images are loaded dynamically based on the product data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please ensure you have proper licensing for any commercial use.
