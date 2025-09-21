# PaperTrail - A Crowd-Powered Study Hub

A comprehensive Django web application for the College of Computer Studies at Cebu Institute of Technology - University, designed to facilitate collaborative learning through shared study resources, interactive quizzes, and digital flashcards.

## Features

### Core Functionality
- **User Authentication**: Secure login/register system with role-based access (User/Admin)
- **Study Resources**: Upload, browse, and share study materials (PDF, PPT, DOCX, e-books)
- **Interactive Quizzes**: Create and take quizzes with multiple-choice questions
- **Digital Flashcards**: Build and study with flashcard sets
- **Rating & Review System**: Rate and review study resources
- **Bookmarking**: Save favorite resources for quick access
- **Search & Filter**: Advanced search functionality with subject and type filters

### Admin Features
- **Admin Dashboard**: Comprehensive overview of platform activity
- **User Management**: Manage user accounts and roles
- **Resource Management**: Approve/reject uploaded resources
- **Content Moderation**: Monitor reviews and ratings
- **Analytics**: View platform statistics and top subjects

## Tech Stack

- **Backend**: Django 4.2.7
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Icons**: Font Awesome 6
- **Forms**: Django Crispy Forms with Bootstrap 5

## Installation

### Prerequisites
- Python 3.8+
- pip
- Supabase account

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PaperTrail
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_NAME=your-supabase-db-name
   DB_USER=your-supabase-user
   DB_PASSWORD=your-supabase-password
   DB_HOST=your-supabase-host
   DB_PORT=5432
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
PaperTrail/
├── accounts/           # User authentication and profiles
├── core/              # Main views and dashboard
├── resources/          # Study resources management
├── quizzes/           # Quiz creation and taking
├── flashcards/        # Flashcard sets management
├── templates/         # HTML templates
├── static/           # CSS, JS, and media files
├── papertrail/       # Django project settings
├── manage.py         # Django management script
└── requirements.txt  # Python dependencies
```

## Database Schema

### Core Models
- **User**: Custom user model with role-based access
- **Resource**: Study materials with metadata
- **Review**: User ratings and comments
- **Bookmark**: Saved resources
- **Quiz**: Interactive quizzes with questions
- **Flashcard**: Digital flashcard sets
- **StudySession**: Learning progress tracking

## Usage

### For Students
1. **Register/Login**: Create an account or log in
2. **Browse Resources**: Search and filter study materials
3. **Upload Content**: Share your study materials
4. **Take Quizzes**: Test your knowledge
5. **Study Flashcards**: Use digital flashcards for memorization
6. **Rate & Review**: Help others find quality resources
7. **Bookmark**: Save resources for later

### For Admins
1. **Access Admin Dashboard**: Monitor platform activity
2. **Manage Users**: View and manage user accounts
3. **Moderate Content**: Approve/reject uploaded resources
4. **Review Moderation**: Monitor ratings and comments
5. **Analytics**: View platform statistics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository.

## Acknowledgments

- College of Computer Studies, Cebu Institute of Technology - University
- Django community for the excellent framework
- Bootstrap team for the responsive UI components
- Font Awesome for the beautiful icons
