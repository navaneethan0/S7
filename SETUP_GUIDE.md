# 🚀 How to Run Smart College Assistant

## Prerequisites
- Python 3.8+ installed
- MySQL 8.0+ installed
- pip (Python package manager)

## Step-by-Step Setup

### 1. 📦 Install Python Dependencies
```bash
# Navigate to project directory
cd "/Users/nandhu/FINAL PROJECT S7"

# Install required packages
pip install -r requirements.txt
```

### 2. 🗄️ Setup MySQL Database
```sql
-- Connect to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE smart_college_assistant;

-- Create user (optional)
CREATE USER 'college_user'@'localhost' IDENTIFIED BY 'college_password';
GRANT ALL PRIVILEGES ON smart_college_assistant.* TO 'college_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. ⚙️ Configure Database Connection
Edit `app.py` line 15:
```python
# Change this line:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/smart_college_assistant'

# To match your MySQL setup:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://college_user:college_password@localhost/smart_college_assistant'
```

### 4. 🚀 Run the Application
```bash
# Start the Flask server
python app.py
```

### 5. 🌐 Access the Application
- **Main Chatbot**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **Default Admin Login**: 
  - Username: `admin`
  - Password: `admin123`

## 🎯 Quick Test

### Test the Chatbot
1. Go to http://localhost:5000
2. Try these example queries:
   - "Where is EW212?"
   - "Show CSE faculty"
   - "Generate MECH timetable"
   - "Hello" (greeting)

### Test Voice Input
1. Click the microphone button
2. Allow microphone access
3. Speak your question
4. See the response!

### Test Dark Mode
1. Click the moon/sun icon in the header
2. Toggle between light and dark themes

### Test Admin Panel
1. Go to http://localhost:5000/admin
2. Login with admin/admin123
3. Explore the dashboard and management features

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Error
```
Error: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server")
```
**Solution**: 
- Make sure MySQL is running
- Check database credentials in app.py
- Verify database exists

#### 2. Module Not Found Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**:
```bash
pip install -r requirements.txt
```

#### 3. Port Already in Use
```
Error: Address already in use
```
**Solution**:
```bash
# Kill process using port 5000
lsof -ti:5000 | xargs kill -9

# Or change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

#### 4. NLTK Data Missing
```
LookupError: Resource punkt not found
```
**Solution**: The app will automatically download NLTK data on first run.

## 📱 Mobile Testing

### Test on Mobile Device
1. Find your computer's IP address:
   ```bash
   ifconfig | grep "inet "
   ```
2. Access from mobile: `http://YOUR_IP:5000`
3. Test voice input and responsive design

## 🎨 Customization

### Change Default Admin Password
Edit `app.py` around line 200:
```python
# Change the default password
admin = Admin(
    username='admin',
    password_hash=generate_password_hash('your_new_password')
)
```

### Add Sample Data
The app automatically creates sample data on first run, but you can add more through the admin panel.

### Customize ML Model
Edit the `IntentClassifier` class in `app.py` to:
- Add new intents
- Modify training data
- Adjust confidence thresholds

## 🚀 Production Deployment

### For Production Use
1. **Set Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key-here
   ```

2. **Use Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Configure Nginx** (optional):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 📊 Monitoring

### Check Application Status
- **Health Check**: http://localhost:5000
- **Admin Dashboard**: http://localhost:5000/admin
- **Database**: Check MySQL for data

### View Logs
```bash
# Application logs
tail -f app.log

# MySQL logs
tail -f /var/log/mysql/error.log
```

## 🎯 Success Indicators

You'll know it's working when:
- ✅ Flask server starts without errors
- ✅ Database tables are created automatically
- ✅ Chatbot responds to queries
- ✅ Voice input works (in supported browsers)
- ✅ Admin panel is accessible
- ✅ Dark mode toggles properly

## 🆘 Need Help?

If you encounter issues:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure MySQL is running
4. Check database connection settings
5. Try accessing the application in a different browser

## 🎉 You're Ready!

Once everything is running:
- **Chatbot**: http://localhost:5000
- **Admin**: http://localhost:5000/admin
- **Default Login**: admin / admin123

Enjoy your Smart College Assistant! 🤖✨

