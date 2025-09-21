# 🚀 PaperTrail Quick Start Guide

## Prerequisites
- Python 3.8+ installed
- pip installed
- Supabase account with database access

## Quick Setup (Recommended)

1. **Run the setup script**:
   ```bash
   python setup.py
   ```

2. **Update your database password** in the `.env` file:
   - Go to your Supabase project dashboard
   - Navigate to Settings > Database
   - Copy your database password
   - Update `DB_PASSWORD` in the `.env` file

3. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Manual Setup (Alternative)

If you prefer manual setup:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create .env file**:
   Copy `env_example.txt` to `.env` and update with your credentials:
   ```bash
   cp env_example.txt .env
   ```

3. **Update .env with your Supabase credentials**:
   ```env
   # Get these from your Supabase project settings
   DB_PASSWORD=your-actual-supabase-db-password
   ```

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start server**:
   ```bash
   python manage.py runserver
   ```

## Getting Your Supabase Database Password

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **Settings** > **Database**
4. Scroll down to **Connection string**
5. Copy the password from the connection string
6. Update `DB_PASSWORD` in your `.env` file

## First Steps After Setup

1. **Access the admin panel** at http://127.0.0.1:8000/admin/
2. **Create test users** with different roles (User/Admin)
3. **Upload sample resources** to test the functionality
4. **Create quizzes and flashcards** to test interactive features
5. **Test the search and filtering** functionality

## Troubleshooting

### Database Connection Issues
- Verify your Supabase credentials in `.env`
- Check that your Supabase project is active
- Ensure the database password is correct

### Migration Issues
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Try running migrations individually: `python manage.py makemigrations accounts`

### Static Files Issues
- Run: `python manage.py collectstatic` (for production)
- Check that `STATIC_URL` and `STATICFILES_DIRS` are configured correctly

## Features to Test

- ✅ User registration and login
- ✅ Resource upload and browsing
- ✅ Quiz creation and taking
- ✅ Flashcard creation and studying
- ✅ Rating and review system
- ✅ Bookmark functionality
- ✅ Admin dashboard
- ✅ Search and filtering

## Support

If you encounter any issues:
1. Check the console output for error messages
2. Verify your `.env` file configuration
3. Ensure all dependencies are installed
4. Check your Supabase project status

Happy studying with PaperTrail! 🎓
