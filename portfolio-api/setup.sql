-- Portfolio Database Setup
-- Run this SQL in your MySQL database (phpMyAdmin or MySQL CLI)

CREATE DATABASE IF NOT EXISTS portfolio_db;
USE portfolio_db;

-- Projects Table
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image VARCHAR(255),
    github_link VARCHAR(255),
    live_link VARCHAR(255),
    tags JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert Sample Projects
INSERT INTO projects (title, description, image, github_link, live_link, tags) VALUES
('RAG Knowledge System', 'Retrieval-Augmented Generation system for intelligent document Q&A with vector embeddings and semantic search capabilities.', 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80', 'https://github.com', '', '["RAG", "LLM", "Python", "Vector DB"]'),

('Real-time Data Pipeline', 'Scalable ETL pipeline processing millions of events daily with Apache Kafka, Spark Streaming, and AWS infrastructure.', 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80', 'https://github.com', '', '["Kafka", "Spark", "Python", "AWS"]'),

('Computer Vision Platform', 'Deep learning platform for image classification and object detection with custom model training and deployment.', 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&q=80', 'https://github.com', 'https://demo.com', '["PyTorch", "CV", "Angular", "FastAPI"]'),

('E-commerce Platform', 'Full-stack e-commerce solution with Angular frontend, Node.js backend, PostgreSQL database, and Stripe payments.', 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&q=80', 'https://github.com', 'https://shop.demo.com', '["Angular", "Node.js", "PostgreSQL", "Stripe"]'),

('Sentiment Analysis API', 'REST API for real-time sentiment analysis using transformer models (BERT) with Docker containerization.', 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&q=80', 'https://github.com', 'https://api.demo.com', '["NLP", "FastAPI", "BERT", "Docker"]'),

('Analytics Dashboard', 'Interactive dashboard for visualizing business metrics with real-time updates using WebSockets.', 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80', 'https://github.com', 'https://dashboard.demo.com', '["React", "D3.js", "Node.js", "MongoDB"]');
