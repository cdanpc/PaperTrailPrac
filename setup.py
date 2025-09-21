#!/usr/bin/env python
"""
Setup script for PaperTrail Django project
"""
import os
import subprocess
import sys

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def setup_environment():
    """Set up the environment for PaperTrail"""
    print("🚀 Setting up PaperTrail Django Project...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        env_content = """# Supabase Configuration
SUPABASE_URL=https://pvtfuyamidbkhjhzkre.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB2dGZ1eWFtaWRia2hqaHprcmUiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTczNzUwMzMyNiwiZXhwIjoxNzY5MDc5MzI2fQ.jMUKU8c8oLNWcQ9hE5akG4Zn7kafxxxxxx

# Django Configuration
SECRET_KEY=django-insecure-change-this-in-production-123456789
DEBUG=True

# Database Configuration (Supabase PostgreSQL)
# Update these with your actual Supabase database credentials
DB_NAME=postgres
DB_USER=postgres.pvtfuyamidbkhjihzkre
DB_PASSWORD=PaperTrail12345678910
DB_HOST=aws-1-ap-southeast-1.pooler.supabase.com
DB_PORT=6543
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
    else:
        print("✅ .env file already exists")
    
    # Install dependencies
    print("📦 Installing dependencies...")
    success, output = run_command("pip install -r requirements.txt")
    if success:
        print("✅ Dependencies installed successfully!")
    else:
        print(f"❌ Error installing dependencies: {output}")
        return False
    
    # Run migrations
    print("🗄️ Running database migrations...")
    success, output = run_command("python manage.py makemigrations")
    if success:
        print("✅ Migrations created successfully!")
    else:
        print(f"❌ Error creating migrations: {output}")
        return False
    
    success, output = run_command("python manage.py migrate")
    if success:
        print("✅ Database migrations completed successfully!")
    else:
        print(f"❌ Error running migrations: {output}")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update your .env file with your actual Supabase database password")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Start the development server: python manage.py runserver")
    print("4. Access the application at: http://127.0.0.1:8000/")
    print("5. Access the admin panel at: http://127.0.0.1:8000/admin/")
    
    return True

if __name__ == "__main__":
    setup_environment()
