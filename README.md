# Smart College Assistant

An intelligent chatbot web application powered by Machine Learning, featuring NLP-based understanding, real-time MySQL database integration, and a comprehensive admin management panel.

## 🚀 Features

### 🤖 **ML-Powered NLP Chatbot**
- **TF-IDF + Logistic Regression** for intent classification
- **Natural Language Processing** with spaCy/NLTK
- **Intent Recognition** for: find_room, faculty_info, timetable, greetings, help
- **Confidence Scoring** for response accuracy

### 🗄️ **Database Integration**
- **MySQL Database** with dynamic data retrieval
- **Real-time Updates** from admin panel
- **Tables**: blocks, faculty, timetable, admin
- **CRUD Operations** for all entities

### 🎨 **Modern UI/UX**
- **WhatsApp-style Chat Interface** with smooth animations
- **Dark Mode Support** with theme persistence
- **Voice Input Recognition** for hands-free interaction
- **Responsive Design** for all devices
- **Auto-complete Suggestions** for better UX

### 👨‍💼 **Admin Panel**
- **Secure Authentication** with password hashing
- **Dashboard** with statistics and quick actions
- **Faculty Management** - Add, edit, delete faculty
- **Block Management** - Manage building blocks
- **Timetable Management** - Schedule classes
- **Real-time Updates** to chatbot responses

## 🛠️ **Technical Stack**

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - ORM for database operations
- **MySQL** - Primary database
- **scikit-learn** - Machine Learning library
- **NLTK/spaCy** - Natural Language Processing

### Frontend
- **HTML5, CSS3, JavaScript** - Core web technologies
- **Font Awesome** - Icons
- **Google Fonts** - Typography
- **Web Speech API** - Voice recognition

### ML Pipeline
- **TF-IDF Vectorization** for text preprocessing
- **Logistic Regression** for intent classification
- **Intent Training** with sample data
- **Confidence Scoring** for responses

## 📋 **Installation & Setup**

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd smart-college-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```sql
CREATE DATABASE smart_college_assistant;
```

### 4. Configure Database
Update the database URI in `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/smart_college_assistant'
```

### 5. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🎯 **Usage Examples**

### Chatbot Interactions
```
User: "Where is EW212?"
Bot: "📍 EW212 is located in AS Block"

User: "Show CSE faculty"
Bot: "👨‍🏫 CSE Faculty:
• Dr. Sasikala D - Professor & Head
• Dr. Premalatha K - Professor
..."

User: "Generate MECH timetable"
Bot: "📅 MECH Timetable:
Monday:
• 9:00-10:00: Thermodynamics - Dr. Mahesh R (ME401)
..."
```

### Admin Panel Features
- **Login**: admin / admin123 (default credentials)
- **Dashboard**: View statistics and quick actions
- **Faculty Management**: Add/edit faculty with contact info
- **Block Management**: Manage building blocks and prefixes
- **Timetable Management**: Schedule classes and subjects

## 🧠 **Machine Learning Pipeline**

### Intent Classification
The system uses a trained ML model to classify user intents:

1. **Text Preprocessing**
   - Tokenization and lowercasing
   - Stop word removal
   - Special character filtering

2. **Feature Extraction**
   - TF-IDF vectorization
   - 1000 most important features

3. **Intent Prediction**
   - Logistic Regression classifier
   - Confidence scoring
   - Intent mapping to responses

### Training Data
```python
training_examples = [
    ("where is ew212", "find_room"),
    ("who teaches ai", "faculty_info"),
    ("show timetable for cse", "timetable"),
    ("hello", "greetings"),
    ("what can you do", "help")
]
```

## 🗄️ **Database Schema**

### Blocks Table
```sql
CREATE TABLE block (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    prefix VARCHAR(10) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Faculty Table
```sql
CREATE TABLE faculty (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    designation VARCHAR(100),
    contact VARCHAR(15),
    room_number VARCHAR(20),
    block_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (block_id) REFERENCES block(id)
);
```

### Timetable Table
```sql
CREATE TABLE timetable (
    id INT PRIMARY KEY AUTO_INCREMENT,
    department VARCHAR(50) NOT NULL,
    day VARCHAR(20) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    faculty_name VARCHAR(100) NOT NULL,
    room_number VARCHAR(20) NOT NULL,
    time_slot VARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🎨 **UI/UX Features**

### Chat Interface
- **WhatsApp-style** message bubbles
- **Typing indicators** with animation
- **Message timestamps** and avatars
- **Quick action buttons** for common queries
- **Auto-scroll** to latest messages

### Voice Input
- **Web Speech API** integration
- **Visual feedback** with pulse animation
- **Error handling** for unsupported browsers
- **Modal interface** for voice controls

### Dark Mode
- **Theme persistence** in localStorage
- **Smooth transitions** between themes
- **Consistent color scheme** across components
- **Toggle button** in header

### Responsive Design
- **Mobile-first** approach
- **Flexible grid layouts**
- **Touch-friendly** interface
- **Optimized for all screen sizes**

## 🔧 **Advanced Features**

### Voice Recognition
```javascript
// Initialize speech recognition
const recognition = new SpeechRecognition();
recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = 'en-US';
```

### Dark Mode Toggle
```javascript
// Toggle dark mode
function toggleDarkMode() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
    localStorage.setItem('darkMode', !isDark);
}
```

### Auto-complete Suggestions
```javascript
// Cycle through helpful hints
const hints = [
    'Try: "Where is ME101?" or "Show ECE faculty"',
    'Ask: "Generate CSE timetable" or "Who teaches AI?"',
    'Say: "Find SF302" or "Show MECH faculty"'
];
```

## 📊 **Admin Panel Features**

### Dashboard
- **Statistics Cards** showing totals
- **Quick Action Buttons** for common tasks
- **System Information** about ML features
- **Real-time Updates** from database

### Faculty Management
- **Add/Edit/Delete** faculty members
- **Department Assignment** and contact info
- **Room Number Mapping** to blocks
- **Bulk Operations** for efficiency

### Timetable Management
- **Schedule Classes** by department
- **Time Slot Management** with validation
- **Faculty Assignment** to subjects
- **Room Allocation** and conflicts

## 🚀 **Deployment**

### Local Development
```bash
python app.py
```

### Production Deployment
1. **Configure MySQL** with production credentials
2. **Set SECRET_KEY** for session security
3. **Use Gunicorn** for WSGI server
4. **Configure Nginx** for reverse proxy
5. **Set up SSL** for HTTPS

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=mysql://user:pass@host:port/db
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 **Acknowledgments**

- **Flask** for the web framework
- **scikit-learn** for machine learning
- **NLTK** for natural language processing
- **Font Awesome** for icons
- **Google Fonts** for typography

## 📞 **Support**

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Smart College Assistant** - Powered by Machine Learning 🤖✨