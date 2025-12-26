from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import pickle
import os
from datetime import datetime
import json
from rapidfuzz import fuzz, process
import spacy
from difflib import SequenceMatcher

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Initialize spaCy model (mandatory)
try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ spaCy model loaded successfully")
except OSError:
    print("❌ ERROR: spaCy English model not found!")
    print("Please install it with: python -m spacy download en_core_web_sm")
    print("The application requires spaCy to function properly.")
    nlp = None
    # Uncomment the line below to make the app fail if spaCy is not available
    # raise RuntimeError("spaCy model is required but not found. Please install it.")

# Initialize stemmer
stemmer = PorterStemmer()

# Enhanced NLP Processing Functions
class EnhancedNLPProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
        self.intent_model = None
        self.faculty_names = []
        self.department_names = []
        self.block_names = []
        self.weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        self.day_aliases = {
            'today': 'today',
            'tomorrow': 'tomorrow',
            'mon': 'Monday','monday':'Monday',
            'tue':'Tuesday','tues':'Tuesday','tuesday':'Tuesday',
            'wed':'Wednesday','wednesday':'Wednesday',
            'thu':'Thursday','thur':'Thursday','thurs':'Thursday','thursday':'Thursday',
            'fri':'Friday','friday':'Friday',
            'sat':'Saturday','saturday':'Saturday',
            'sun':'Sunday','sunday':'Sunday'
        }
        
    def preprocess_text(self, text):
        """Enhanced text preprocessing with stemming and normalization"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and stem
        processed_tokens = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                stemmed = stemmer.stem(token)
                processed_tokens.append(stemmed)
        
        return ' '.join(processed_tokens)
    
    def extract_entities(self, text):
        """Extract named entities using spaCy"""
        entities = {
            'names': [],
            'departments': [],
            'rooms': [],
            'blocks': []
        }
        
        if nlp:
            try:
                doc = nlp(text)
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        entities['names'].append(ent.text)
                    elif ent.label_ in ["ORG", "GPE"]:
                        entities['departments'].append(ent.text)
            except Exception as e:
                # If spaCy processing fails, continue without entity extraction
                print(f"spaCy entity extraction error: {e}")
        
        # Extract room numbers and block codes
        room_pattern = r'\b[A-Z]{2}\d{3}\b'
        rooms = re.findall(room_pattern, text.upper())
        entities['rooms'].extend(rooms)
        
        # Extract block prefixes
        block_pattern = r'\b(EW|WW|SF|ME|AE|AS)\b'
        blocks = re.findall(block_pattern, text.upper())
        entities['blocks'].extend(blocks)
        
        return entities
    
    def fuzzy_match_faculty(self, query, faculty_list, threshold=60):
        """Find best matching faculty using fuzzy string matching"""
        if not faculty_list:
            return None, 0
        
        # Extract potential names from query
        entities = self.extract_entities(query)
        query_names = entities['names']
        
        # If no names extracted, use the whole query
        if not query_names:
            query_names = [query]
        
        best_match = None
        best_score = 0
        
        for faculty in faculty_list:
            faculty_name = faculty.name.lower()
            
            # Try matching with each extracted name
            for query_name in query_names:
                # Multiple fuzzy matching algorithms
                ratio_score = fuzz.ratio(query_name.lower(), faculty_name)
                partial_score = fuzz.partial_ratio(query_name.lower(), faculty_name)
                token_sort_score = fuzz.token_sort_ratio(query_name.lower(), faculty_name)
                token_set_score = fuzz.token_set_ratio(query_name.lower(), faculty_name)
                
                # Weighted combination of scores
                combined_score = (
                    ratio_score * 0.3 +
                    partial_score * 0.3 +
                    token_sort_score * 0.2 +
                    token_set_score * 0.2
                )
                
                if combined_score > best_score and combined_score >= threshold:
                    best_score = combined_score
                    best_match = faculty
        
        return best_match, best_score
    
    def fuzzy_match_department(self, query, department_list, threshold=60):
        """Find best matching department using fuzzy string matching"""
        if not department_list:
            return None, 0
        
        # Department mapping for common variations
        dept_mapping = {
            'cse': ['computer science', 'cs', 'computer', 'computing'],
            'ece': ['electronics', 'electrical', 'electronics and communication'],
            'mech': ['mechanical', 'mech', 'mechanical engineering'],
            'ae': ['aerospace', 'aeronautical', 'aerospace engineering'],
            'it': ['information technology', 'information tech'],
            'aids': ['artificial intelligence', 'ai', 'data science', 'ai and data science']
        }
        
        query_lower = query.lower().strip()
        best_match = None
        best_score = 0
        
        for dept in department_list:
            dept_lower = dept.lower()
            
            # Direct matching
            if query_lower in dept_lower or dept_lower in query_lower:
                return dept, 100
            
            # Check mapping
            for key, variations in dept_mapping.items():
                if key in query_lower:
                    for variation in variations:
                        if variation in dept_lower:
                            return dept, 90
            
            # Fuzzy matching
            score = fuzz.ratio(query_lower, dept_lower)
            if score > best_score and score >= threshold:
                best_score = score
                best_match = dept
        
        return best_match, best_score
    
    def semantic_search_faculty(self, query, faculty_list, threshold=0.6):
        """Semantic search using TF-IDF and cosine similarity"""
        if not faculty_list or not query:
            return None, 0
        
        # Prepare faculty data for vectorization
        faculty_texts = []
        faculty_objects = []
        
        for faculty in faculty_list:
            # Create searchable text combining name, department, designation
            searchable_text = f"{faculty.name} {faculty.department} {faculty.designation or ''}"
            faculty_texts.append(searchable_text)
            faculty_objects.append(faculty)
        
        # Add query to the list
        all_texts = faculty_texts + [query]
        
        # Vectorize
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(all_texts)
        
        # Calculate cosine similarity
        query_vector = tfidf_matrix[-1]  # Last vector is the query
        faculty_vectors = tfidf_matrix[:-1]  # All except last are faculty
        
        similarities = cosine_similarity(query_vector, faculty_vectors)[0]
        
        # Find best match
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        
        if best_score >= threshold:
            return faculty_objects[best_idx], best_score
        
        return None, best_score
    
    def extract_day(self, text):
        text_low = text.lower()
        # direct weekday names
        for day in self.weekdays:
            if day.lower() in text_low:
                return day
        # aliases like today/tomorrow and short forms
        for key, mapped in self.day_aliases.items():
            if re.search(r'\b' + re.escape(key) + r'\b', text_low):
                return mapped
        return None

    def enhanced_intent_classification(self, query):
        """Enhanced intent classification with multiple features"""
        if not query:
            return "greeting", 0.0
        
        # Preprocess query
        processed_query = self.preprocess_text(query)
        
        # Extract entities
        entities = self.extract_entities(query)
        
        # Intent patterns
        intent_patterns = {
            'faculty_info': [
                r'\b(faculty|teacher|professor|staff|contact|details|info)\b',
                r'\b(who is|tell me about|show me|find)\b',
                r'\b(phone|email|contact|room)\b'
            ],
            'timetable_info': [
                r'\b(timetable|time table|schedule|class(?:es)?|period|slot|slots)\b',
                r'\b(today|tomorrow|day after tomorrow)\b',
                r'\b(when|what time|which period)\b',
                r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
                r'\b(generate|show|get|display|view)\b.*\b(timetable|schedule|class)\b',
                r'\b(cse|ece|mech|ae|it|aids)\b.*\b(timetable|schedule)\b'
            ],
            'location_query': [
                r'\b(where|location|find|locate)\b',
                r'\b(room|classroom|hall|block)\b',
                r'\b(EW|WW|SF|ME|AE|AS)\d{3}\b'
            ],
            'greeting': [
                r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b',
                r'\b(help|assist|support)\b'
            ],
            'department_info': [
                r'\b(department|dept|branch|course)\b',
                r'\b(cse|ece|mech|ae|it|aids)\b',
                r'\b(computer|electronics|mechanical|aerospace|information)\b'
            ]
        }
        
        # Calculate pattern scores
        intent_scores = {}
        for intent, patterns in intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, query.lower()))
                score += matches
            intent_scores[intent] = score
        
        # Boost scores based on entities
        if entities['names']:
            intent_scores['faculty_info'] += 2
        if entities['rooms'] or entities['blocks']:
            intent_scores['location_query'] += 2
        if entities['departments']:
            intent_scores['department_info'] += 1
        
        # Find best intent
        if not intent_scores or max(intent_scores.values()) == 0:
            return "greeting", 0.5
        
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(intent_scores[best_intent] / 5.0, 1.0)  # Normalize to 0-1
        
        return best_intent, confidence

# Initialize enhanced NLP processor
nlp_processor = EnhancedNLPProcessor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Configure database path - use instance folder for persistence on Render
import os
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)
db_path = os.path.join(instance_path, 'smart_college_assistant.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    prefix = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    designation = db.Column(db.String(100))
    contact = db.Column(db.String(15))
    room_number = db.Column(db.String(20))
    block_id = db.Column(db.Integer, db.ForeignKey('block.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    faculty_name = db.Column(db.String(100), nullable=False)
    room_number = db.Column(db.String(20), nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# NLP Intent Classification
class IntentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.classifier = LogisticRegression()
        self.intents = {
            'find_room': ['where is', 'locate', 'find', 'room', 'classroom', 'location'],
            'faculty_info': ['who teaches', 'faculty', 'professor', 'teacher', 'contact', 'staff'],
            'timetable': ['timetable', 'schedule', 'class', 'today', 'time', 'schedule'],
            'greetings': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'help': ['help', 'what can you do', 'how to use', 'assistance', 'support']
        }
        self.trained = False

    def preprocess_text(self, text):
        """Preprocess text for NLP"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        return ' '.join(tokens)

    def create_training_data(self):
        """Create training data for intent classification"""
        training_data = []
        labels = []
        
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                training_data.append(keyword)
                labels.append(intent)
        
        # Add more training examples
        training_examples = [
            ("where is ew212", "find_room"),
            ("locate me101", "find_room"),
            ("find ae205", "find_room"),
            ("where can i find sf302", "find_room"),
            ("who teaches ai", "faculty_info"),
            ("give contact of dr priya", "faculty_info"),
            ("faculty for data science", "faculty_info"),
            ("show timetable for cse", "timetable"),
            ("today's class for mechanical", "timetable"),
            ("as block schedule", "timetable"),
            ("hello", "greetings"),
            ("hi", "greetings"),
            ("hey assistant", "greetings"),
            ("what can you do", "help"),
            ("how to use this bot", "help")
        ]
        
        for text, intent in training_examples:
            training_data.append(text)
            labels.append(intent)
        
        return training_data, labels

    def train(self):
        """Train the intent classifier"""
        training_data, labels = self.create_training_data()
        
        # Preprocess training data
        processed_data = [self.preprocess_text(text) for text in training_data]
        
        # Vectorize
        X = self.vectorizer.fit_transform(processed_data)
        
        # Train classifier
        self.classifier.fit(X, labels)
        self.trained = True
        
        # Save model
        with open('intent_model.pkl', 'wb') as f:
            pickle.dump((self.vectorizer, self.classifier), f)

    def predict_intent(self, text):
        """Predict intent for given text"""
        if not self.trained:
            self.train()
        
        processed_text = self.preprocess_text(text)
        X = self.vectorizer.transform([processed_text])
        intent = self.classifier.predict(X)[0]
        confidence = self.classifier.predict_proba(X).max()
        
        return intent, confidence

# Initialize intent classifier
intent_classifier = IntentClassifier()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_login():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    username = request.form['username']
    password = request.form['password']
    
    admin = Admin.query.filter_by(username=username).first()
    
    if admin and check_password_hash(admin.password_hash, password):
        session['admin_logged_in'] = True
        session['admin_username'] = username
        flash('Login successful!', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid credentials!', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    # Get statistics
    total_blocks = Block.query.count()
    total_faculty = Faculty.query.count()
    total_timetable_entries = Timetable.query.count()
    
    return render_template('admin_dashboard.html', 
                         total_blocks=total_blocks,
                         total_faculty=total_faculty,
                         total_timetable_entries=total_timetable_entries)

@app.route('/admin/blocks')
def admin_blocks():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    try:
        # Ensure database is initialized
        db.create_all()
        
        blocks = Block.query.all()
        print(f"Retrieved {len(blocks)} blocks")
        return render_template('admin_blocks.html', blocks=blocks)
    except Exception as e:
        print(f"Database query error in admin_blocks: {e}")
        import traceback
        traceback.print_exc()
        return render_template('admin_blocks.html', blocks=[])

@app.route('/admin/faculty')
def admin_faculty():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    try:
        # Ensure database is initialized
        db.create_all()
        
        faculty = Faculty.query.all()
        blocks = Block.query.all()
        print(f"Retrieved {len(faculty)} faculty and {len(blocks)} blocks")
        return render_template('admin_faculty.html', faculty=faculty, blocks=blocks)
    except Exception as e:
        print(f"Database query error in admin_faculty: {e}")
        import traceback
        traceback.print_exc()
        # Return empty lists if database query fails
        return render_template('admin_faculty.html', faculty=[], blocks=[])

@app.route('/admin/timetable')
def admin_timetable():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    try:
        # Ensure database is initialized
        db.create_all()
        
        timetable = Timetable.query.all()
        faculty = Faculty.query.all()
        print(f"Retrieved {len(timetable)} timetable entries and {len(faculty)} faculty")
        return render_template('admin_timetable.html', timetable=timetable, faculty=faculty)
    except Exception as e:
        print(f"Database query error in admin_timetable: {e}")
        import traceback
        traceback.print_exc()
        return render_template('admin_timetable.html', timetable=[], faculty=[])

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('admin_login'))

# API Routes
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        print(f"📨 Received message: '{user_message}'")
        
        # Use enhanced NLP processing
        try:
            intent, confidence = nlp_processor.enhanced_intent_classification(user_message)
            print(f"🎯 Intent detected: {intent} (confidence: {confidence:.2f})")
        except Exception as e:
            # Fallback to basic intent detection if NLP fails
            print(f"❌ NLP processing error: {e}")
            import traceback
            traceback.print_exc()
            # Try to detect intent manually
            user_lower = user_message.lower()
            if any(word in user_lower for word in ['faculty', 'teacher', 'professor', 'staff']):
                intent = 'faculty_info'
            elif any(word in user_lower for word in ['where', 'locate', 'find', 'room', 'ew', 'me', 'sf', 'ww', 'ae']):
                intent = 'location_query'
            elif any(word in user_lower for word in ['timetable', 'schedule', 'class', 'time']):
                intent = 'timetable_info'
            else:
                intent = 'greeting'
            confidence = 0.5
            print(f"🔄 Fallback intent: {intent}")
        
        try:
            response = handle_intent_enhanced(intent, user_message, confidence)
            print(f"✅ Response generated: {response[:50]}...")
        except Exception as e:
            # Fallback response if intent handling fails
            print(f"❌ Intent handling error: {e}")
            import traceback
            traceback.print_exc()
            # Try to handle based on keywords even if handler fails
            user_lower = user_message.lower()
            if 'faculty' in user_lower or 'cse' in user_lower or 'ece' in user_lower:
                response = "I'm having trouble accessing the faculty database. Please try again later."
            elif 'ew' in user_lower or 'me' in user_lower or 'room' in user_lower:
                response = "I'm having trouble finding room information. Please check the room code format (e.g., EW212)."
            elif intent == 'greeting':
                response = handle_greetings()
            else:
                response = "I'm here to help! Could you please rephrase your question?"
        
        return jsonify({
            'response': response,
            'intent': intent,
            'confidence': float(confidence)
        })
    except Exception as e:
        # Catch any other unexpected errors
        print(f"❌ Chat endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'response': "I'm sorry, I encountered an error. Please try again or rephrase your question.",
            'intent': 'error',
            'confidence': 0.0
        }), 200  # Return 200 so frontend doesn't treat it as HTTP error

def handle_intent_enhanced(intent, message, confidence):
    """Enhanced intent handler with fuzzy matching and semantic search"""
    
    print(f"🔧 Handling intent: {intent} for message: '{message}'")
    
    try:
        if intent == 'location_query':
            return handle_find_room_enhanced(message)
        elif intent == 'faculty_info':
            return handle_faculty_info_enhanced(message)
        elif intent == 'timetable_info':
            return handle_timetable_enhanced(message)
        elif intent == 'department_info':
            return handle_department_info_enhanced(message)
        elif intent == 'greeting':
            return handle_greetings()
        else:
            # Try to infer intent from message content
            message_lower = message.lower()
            if any(word in message_lower for word in ['faculty', 'teacher', 'professor', 'cse', 'ece', 'mech']):
                print("🔄 Inferring faculty_info from message content")
                return handle_faculty_info_enhanced(message)
            elif any(word in message_lower for word in ['where', 'locate', 'find', 'ew', 'me', 'sf', 'room']):
                print("🔄 Inferring location_query from message content")
                return handle_find_room_enhanced(message)
            elif any(word in message_lower for word in ['timetable', 'schedule', 'class', 'time table', 'generate', 'show timetable']):
                print("🔄 Inferring timetable_info from message content")
                return handle_timetable_enhanced(message)
            else:
                return "I'm not sure how to help with that. Could you please rephrase your question?"
    except Exception as e:
        print(f"❌ Error in handle_intent_enhanced: {e}")
        import traceback
        traceback.print_exc()
        raise  # Re-raise to be caught by caller

def handle_intent(intent, message, confidence):
    """Handle different intents and return appropriate responses"""
    
    if intent == 'find_room':
        return handle_find_room(message)
    elif intent == 'faculty_info':
        return handle_faculty_info(message)
    elif intent == 'timetable':
        return handle_timetable(message)
    elif intent == 'greetings':
        return handle_greetings()
    elif intent == 'help':
        return handle_help()
    else:
        return "I'm not sure how to help with that. Could you please rephrase your question?"

def handle_find_room(message):
    """Handle room location queries"""
    # Extract room code from message
    room_match = re.search(r'([A-Z]{2}\d{3})', message.upper())
    if not room_match:
        return "Please provide a valid room code (e.g., EW212, ME101, SF302)"
    
    room_code = room_match.group(1)
    prefix = room_code[:2]
    
    block = Block.query.filter_by(prefix=prefix).first()
    if block:
        return f"📍 **{room_code}** is located in **{block.name}**"
    else:
        return f"❌ Sorry, I couldn't find information for room {room_code}"

def handle_faculty_info(message):
    """Handle faculty information queries"""
    # Extract department or faculty name
    departments = ['cse', 'ece', 'mech', 'ae', 'it', 'aids']
    department = None
    
    for dept in departments:
        if dept in message.lower():
            department = dept.upper()
            break
    
    if department:
        faculty = Faculty.query.filter_by(department=department).all()
        if faculty:
            response = f"👨‍🏫 **{department} Faculty:**\n\n"
            for f in faculty:
                response += f"• **{f.name}** - {f.designation}\n"
                if f.contact:
                    response += f"  📞 {f.contact}\n"
                if f.room_number:
                    response += f"  🏢 Room: {f.room_number}\n"
                response += "\n"
            return response
        else:
            return f"No faculty found for {department} department"
    else:
        return "Please specify a department (CSE, ECE, MECH, AE, IT, AIDS) to get faculty information"

def handle_timetable(message):
    """Handle timetable queries"""
    departments = ['cse', 'ece', 'mech', 'ae', 'it', 'aids']
    department = None
    
    for dept in departments:
        if dept in message.lower():
            department = dept.upper()
            break
    
    if department:
        timetable = Timetable.query.filter_by(department=department).all()
        if timetable:
            response = f"📅 **{department} Timetable:**\n\n"
            current_day = None
            for entry in timetable:
                if entry.day != current_day:
                    response += f"\n**{entry.day}:**\n"
                    current_day = entry.day
                response += f"• {entry.time_slot}: {entry.subject} - {entry.faculty_name} ({entry.room_number})\n"
            return response
        else:
            return f"No timetable found for {department} department"
    else:
        return "Please specify a department (CSE, ECE, MECH, AE, IT, AIDS) to get timetable information"

def handle_greetings():
    """Handle greeting messages"""
    greetings = [
        "👋 Hello! I'm your Smart College Assistant. How can I help you today?",
        "👋 Hi there! I can help you find classrooms, faculty info, and timetables. What do you need?",
        "👋 Hey! Welcome to the Smart College Assistant. What can I do for you?"
    ]
    import random
    return random.choice(greetings)

def handle_help():
    """Handle help requests"""
    return """
🤖 **Smart College Assistant - What I can do:**

📍 **Find Classrooms:** Ask "Where is EW212?" or "Locate ME101"
👨‍🏫 **Faculty Info:** Ask "Show CSE faculty" or "Who teaches AI?"
📅 **Timetables:** Ask "Show CSE timetable" or "Today's schedule"
❓ **Help:** Ask "What can you do?" or "How to use this bot?"

**Quick Actions:**
• Use the buttons below for common queries
• Try voice input for hands-free interaction
• Switch to dark mode for comfortable viewing

**Examples:**
• "Where is SF302?"
• "Show ECE faculty"
• "Generate MECH timetable"
• "Who teaches Machine Learning?"
"""

# Enhanced Handler Functions with Fuzzy Matching and Semantic Search
def handle_find_room_enhanced(message):
    """Enhanced room location queries with fuzzy matching"""
    try:
        # Ensure database is initialized
        with app.app_context():
            db.create_all()
        
        entities = nlp_processor.extract_entities(message)
        print(f"🔍 Extracted entities: {entities}")
        
        # Check for room codes in entities
        if entities['rooms']:
            room_code = entities['rooms'][0]
            prefix = room_code[:2]
            print(f"🔍 Looking for room {room_code} with prefix {prefix}")
            
            try:
                with app.app_context():
                    block = Block.query.filter_by(prefix=prefix).first()
                    print(f"🔍 Block query result: {block}")
                    if block:
                        return f"📍 **{room_code}** is located in **{block.name}**\n\n{block.description or 'No additional information available.'}"
                    else:
                        # Check if any blocks exist
                        block_count = Block.query.count()
                        print(f"⚠️ No block found for prefix {prefix}. Total blocks in DB: {block_count}")
                        return f"❌ Sorry, I couldn't find information for room {room_code}. Available blocks: {', '.join([b.prefix for b in Block.query.all()]) if block_count > 0 else 'None'}"
            except Exception as e:
                print(f"❌ Database query error in handle_find_room_enhanced: {e}")
                import traceback
                traceback.print_exc()
                return f"Please provide a valid room code (e.g., EW212, ME101, SF302)"
        
        # Check for block prefixes
        if entities['blocks']:
            block_prefix = entities['blocks'][0]
            try:
                with app.app_context():
                    block = Block.query.filter_by(prefix=block_prefix).first()
                    if block:
                        return f"📍 **{block_prefix} Block** refers to **{block.name}**\n\n{block.description or 'No additional information available.'}"
            except Exception as e:
                print(f"❌ Database query error: {e}")
                import traceback
                traceback.print_exc()
        
        # Try to extract room code directly from message if entities didn't catch it
        import re
        room_match = re.search(r'\b([A-Z]{2}\d{3})\b', message.upper())
        if room_match:
            room_code = room_match.group(1)
            prefix = room_code[:2]
            print(f"🔍 Direct regex match found room {room_code}")
            try:
                with app.app_context():
                    block = Block.query.filter_by(prefix=prefix).first()
                    if block:
                        return f"📍 **{room_code}** is located in **{block.name}**\n\n{block.description or 'No additional information available.'}"
            except Exception as e:
                print(f"❌ Database query error: {e}")
        
        return "Please provide a valid room code (e.g., EW212, ME101, SF302) or block prefix (EW, WW, SF, ME, AE, AS)"
    except Exception as e:
        print(f"❌ Error in handle_find_room_enhanced: {e}")
        import traceback
        traceback.print_exc()
        return "I'm having trouble processing your request. Please try again with a room code like EW212 or ME101."

def handle_faculty_info_enhanced(message):
    """Enhanced faculty information with fuzzy matching and semantic search"""
    try:
        # Ensure database is initialized
        with app.app_context():
            db.create_all()
        
        # Get all faculty from database
        try:
            with app.app_context():
                all_faculty = Faculty.query.all()
                faculty_count = len(all_faculty)
                print(f"🔍 Retrieved {faculty_count} faculty from database")
        except Exception as e:
            print(f"❌ Database query error: {e}")
            import traceback
            traceback.print_exc()
            return "I'm having trouble accessing the faculty database. Please try again later."
        
        if not all_faculty:
            print("⚠️ No faculty found in database")
            return "No faculty information available in the database. Please add faculty through the admin panel."
        
        # Try fuzzy matching first
        try:
            fuzzy_match, fuzzy_score = nlp_processor.fuzzy_match_faculty(message, all_faculty, threshold=50)
        except Exception as e:
            print(f"Fuzzy matching error: {e}")
            fuzzy_match, fuzzy_score = None, 0
        
        # Try semantic search
        try:
            semantic_match, semantic_score = nlp_processor.semantic_search_faculty(message, all_faculty, threshold=0.4)
        except Exception as e:
            print(f"Semantic search error: {e}")
            semantic_match, semantic_score = None, 0
        
        # Choose the best match
        best_match = None
        match_type = ""
        
        if fuzzy_match and fuzzy_score >= 60:
            best_match = fuzzy_match
            match_type = f"fuzzy match (score: {fuzzy_score:.1f}%)"
        elif semantic_match and semantic_score >= 0.5:
            best_match = semantic_match
            match_type = f"semantic match (score: {semantic_score:.1f})"
        
        if best_match:
            response = f"👨‍🏫 **Faculty Found** ({match_type}):\n\n"
            response += f"**Name:** {best_match.name}\n"
            response += f"**Department:** {best_match.department}\n"
            if best_match.designation:
                response += f"**Designation:** {best_match.designation}\n"
            if best_match.contact:
                response += f"**Contact:** {best_match.contact}\n"
            if best_match.room_number:
                response += f"**Room:** {best_match.room_number}\n"
            
            return response
        
        # If no specific match, try department-based search
        try:
            entities = nlp_processor.extract_entities(message)
            departments = ['CSE', 'ECE', 'MECH', 'AE', 'IT', 'AIDS']
            
            # Check for department mentions
            found_dept = None
            for dept in departments:
                if dept.lower() in message.lower() or any(dept.lower() in word.lower() for word in message.split()):
                    found_dept = dept
                    break
            
            if found_dept:
                try:
                    with app.app_context():
                        faculty = Faculty.query.filter_by(department=found_dept).all()
                        print(f"🔍 Found {len(faculty)} faculty for department {found_dept}")
                        if faculty:
                            response = f"👨‍🏫 **{found_dept} Faculty:**\n\n"
                            for f in faculty:
                                response += f"• **{f.name}** - {f.designation or 'Faculty'}\n"
                                if f.contact:
                                    response += f"  📞 {f.contact}\n"
                                if f.room_number:
                                    response += f"  🏢 Room: {f.room_number}\n"
                                response += "\n"
                            return response
                        else:
                            return f"No faculty found for {found_dept} department. Please add faculty through the admin panel."
                except Exception as e:
                    print(f"❌ Department query error: {e}")
                    import traceback
                    traceback.print_exc()
        except Exception as e:
            print(f"Entity extraction error: {e}")
        
        return "I couldn't find a specific faculty member. Please try:\n• Providing a more specific name\n• Mentioning the department (CSE, ECE, MECH, AE, IT, AIDS)\n• Using partial names (e.g., 'Pri' for 'Priya')"
    except Exception as e:
        print(f"Error in handle_faculty_info_enhanced: {e}")
        return "I'm having trouble accessing faculty information. Please try again later."

def handle_timetable_enhanced(message):
    """Enhanced timetable queries with fuzzy department and day matching"""
    try:
        print(f"📅 Processing timetable query: '{message}'")
        
        # Ensure database is initialized
        with app.app_context():
            db.create_all()
            # Check if timetable table has any data
            total_entries = Timetable.query.count()
            print(f"📊 Total timetable entries in database: {total_entries}")
        
        # Determine department
        departments = ['CSE', 'ECE', 'MECH', 'AE', 'IT', 'AIDS']
        found_dept = None
        message_lower = message.lower()
        
        # Direct department matching
        for dept in departments:
            if dept.lower() in message_lower:
                found_dept = dept
                print(f"✅ Found department: {found_dept}")
                break
        
        # Try fuzzy matching if not found
        if not found_dept:
            try:
                dept_list = [dept.lower() for dept in departments]
                fuzzy_dept, score = nlp_processor.fuzzy_match_department(message, dept_list, threshold=50)
                if fuzzy_dept:
                    found_dept = fuzzy_dept.upper()
                    print(f"✅ Fuzzy matched department: {found_dept} (score: {score})")
            except Exception as e:
                print(f"⚠️ Fuzzy department matching error: {e}")

        if not found_dept:
            print("❌ No department found in message")
            return "Please specify a department (CSE, ECE, MECH, AE, IT, AIDS) to get timetable information"

        # Determine day
        try:
            extracted_day = nlp_processor.extract_day(message)
            if extracted_day in (None, ''):
                day = datetime.now().strftime('%A')
            elif extracted_day == 'today':
                day = datetime.now().strftime('%A')
            elif extracted_day == 'tomorrow':
                day = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + pd.Timedelta(days=1)).strftime('%A')
            else:
                day = extracted_day
        except Exception as e:
            print(f"Day extraction error: {e}")
            day = datetime.now().strftime('%A')

        # Fetch timetable for department and day, ordered by time_slot
        try:
            with app.app_context():
                # First, check all entries for the department
                all_dept_entries = Timetable.query.filter_by(department=found_dept).all()
                print(f"🔍 Total entries for {found_dept}: {len(all_dept_entries)}")
                
                if all_dept_entries:
                    # Show available days
                    available_days = set([e.day for e in all_dept_entries])
                    print(f"📅 Available days for {found_dept}: {available_days}")
                
                # Query for specific day
                entries = (Timetable.query
                           .filter_by(department=found_dept, day=day)
                           .order_by(Timetable.time_slot.asc())
                           .all())
                print(f"🔍 Found {len(entries)} timetable entries for {found_dept} on {day}")
        except Exception as e:
            print(f"❌ Timetable query error: {e}")
            import traceback
            traceback.print_exc()
            return "I'm having trouble accessing the timetable database. Please try again later."

        if not entries:
            # Check if there are any entries for this department on other days
            with app.app_context():
                other_day_entries = Timetable.query.filter_by(department=found_dept).all()
                if other_day_entries:
                    available_days = set([e.day for e in other_day_entries])
                    return f"No classes scheduled for {day} in {found_dept} department.\n\nAvailable days: {', '.join(sorted(available_days))}\n\nPlease add timetable entries for {day} through the admin panel."
                else:
                    return f"No timetable entries found for {found_dept} department. Please add timetable entries through the admin panel."

        # Format response
        response_lines = [f"📅 **{found_dept} - {day} Timetable:**\n"]
        for e in entries:
            response_lines.append(
                f"• Time: {e.time_slot} | Subject: {e.subject} | Faculty: {e.faculty_name} | Room: {e.room_number}"
            )
        return "\n".join(response_lines)
    except Exception as e:
        print(f"Error in handle_timetable_enhanced: {e}")
        return "I'm having trouble processing your timetable request. Please try again later."

def handle_department_info_enhanced(message):
    """Enhanced department information with fuzzy matching"""
    entities = nlp_processor.extract_entities(message)
    
    # Try to find department
    departments = ['CSE', 'ECE', 'MECH', 'AE', 'IT', 'AIDS']
    found_dept = None
    
    # Check for exact department matches
    for dept in departments:
        if dept.lower() in message.lower():
            found_dept = dept
            break
    
    # If no exact match, try fuzzy matching
    if not found_dept:
        dept_list = [dept.lower() for dept in departments]
        fuzzy_dept, fuzzy_score = nlp_processor.fuzzy_match_department(message, dept_list, threshold=50)
        if fuzzy_dept:
            found_dept = fuzzy_dept.upper()
    
    if found_dept:
        # Get faculty count for the department
        faculty_count = Faculty.query.filter_by(department=found_dept).count()
        
        response = f"🏛️ **{found_dept} Department Information:**\n\n"
        response += f"**Faculty Count:** {faculty_count}\n\n"
        
        # Get some sample faculty
        sample_faculty = Faculty.query.filter_by(department=found_dept).limit(3).all()
        if sample_faculty:
            response += "**Sample Faculty:**\n"
            for faculty in sample_faculty:
                response += f"• {faculty.name} - {faculty.designation or 'Faculty'}\n"
        
        return response
    
    return "Please specify a department (CSE, ECE, MECH, AE, IT, AIDS) to get department information"

# Auto-suggestion API endpoint
@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    """Get auto-suggestions for user input"""
    query = request.json.get('query', '').strip()
    
    if not query or len(query) < 2:
        return jsonify({'suggestions': []})
    
    suggestions = []
    
    # Get faculty suggestions
    all_faculty = Faculty.query.all()
    if all_faculty:
        faculty_names = [f.name for f in all_faculty]
        faculty_matches = process.extract(query, faculty_names, limit=5, scorer=fuzz.partial_ratio)
        for match, score, _ in faculty_matches:
            if score >= 60:
                suggestions.append({
                    'text': match,
                    'type': 'faculty',
                    'score': score
                })
    
    # Get department suggestions
    departments = ['CSE', 'ECE', 'MECH', 'AE', 'IT', 'AIDS']
    dept_matches = process.extract(query, departments, limit=3, scorer=fuzz.partial_ratio)
    for match, score, _ in dept_matches:
        if score >= 50:
            suggestions.append({
                'text': match,
                'type': 'department',
                'score': score
            })
    
    # Get room suggestions
    room_patterns = ['EW', 'WW', 'SF', 'ME', 'AE', 'AS']
    for prefix in room_patterns:
        if prefix.lower() in query.lower():
            suggestions.append({
                'text': f"{prefix}XXX",
                'type': 'room',
                'score': 80
            })
    
    # Sort by score and limit to 8 suggestions
    suggestions.sort(key=lambda x: x['score'], reverse=True)
    suggestions = suggestions[:8]
    
    return jsonify({'suggestions': suggestions})

# Admin API Routes
@app.route('/api/admin/blocks', methods=['GET', 'POST'])
def api_blocks():
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        blocks = Block.query.all()
        return jsonify([{
            'id': block.id,
            'name': block.name,
            'prefix': block.prefix,
            'description': block.description
        } for block in blocks])
    
    elif request.method == 'POST':
        data = request.json
        block = Block(
            name=data['name'],
            prefix=data['prefix'],
            description=data.get('description', '')
        )
        db.session.add(block)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Block added successfully'})

@app.route('/api/admin/blocks/<int:block_id>', methods=['PUT', 'DELETE'])
def api_block_by_id(block_id):
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    block = Block.query.get_or_404(block_id)
    
    if request.method == 'PUT':
        data = request.json
        block.name = data['name']
        block.prefix = data['prefix']
        block.description = data.get('description', '')
        db.session.commit()
        return jsonify({'success': True, 'message': 'Block updated successfully'})
    
    elif request.method == 'DELETE':
        db.session.delete(block)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Block deleted successfully'})

@app.route('/api/admin/faculty', methods=['GET', 'POST'])
def api_faculty():
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        faculty = Faculty.query.all()
        return jsonify([{
            'id': f.id,
            'name': f.name,
            'department': f.department,
            'designation': f.designation,
            'contact': f.contact,
            'room_number': f.room_number,
            'block_id': f.block_id
        } for f in faculty])
    
    elif request.method == 'POST':
        data = request.json
        faculty = Faculty(
            name=data['name'],
            department=data['department'],
            designation=data.get('designation', ''),
            contact=data.get('contact', ''),
            room_number=data.get('room_number', ''),
            block_id=data.get('block_id') if data.get('block_id') else None
        )
        db.session.add(faculty)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Faculty added successfully'})

@app.route('/api/admin/faculty/<int:faculty_id>', methods=['PUT', 'DELETE'])
def api_faculty_by_id(faculty_id):
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    faculty = Faculty.query.get_or_404(faculty_id)
    
    if request.method == 'PUT':
        data = request.json
        faculty.name = data['name']
        faculty.department = data['department']
        faculty.designation = data.get('designation', '')
        faculty.contact = data.get('contact', '')
        faculty.room_number = data.get('room_number', '')
        faculty.block_id = data.get('block_id') if data.get('block_id') else None
        db.session.commit()
        return jsonify({'success': True, 'message': 'Faculty updated successfully'})
    
    elif request.method == 'DELETE':
        db.session.delete(faculty)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Faculty deleted successfully'})

@app.route('/api/admin/timetable', methods=['GET', 'POST'])
def api_timetable():
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        timetable = Timetable.query.all()
        return jsonify([{
            'id': t.id,
            'department': t.department,
            'day': t.day,
            'subject': t.subject,
            'faculty_name': t.faculty_name,
            'room_number': t.room_number,
            'time_slot': t.time_slot
        } for t in timetable])
    
    elif request.method == 'POST':
        data = request.json
        timetable = Timetable(
            department=data['department'],
            day=data['day'],
            subject=data['subject'],
            faculty_name=data['faculty_name'],
            room_number=data['room_number'],
            time_slot=data['time_slot']
        )
        db.session.add(timetable)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Timetable entry added successfully'})

@app.route('/api/admin/timetable/<int:timetable_id>', methods=['PUT', 'DELETE'])
def api_timetable_by_id(timetable_id):
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    timetable = Timetable.query.get_or_404(timetable_id)
    
    if request.method == 'PUT':
        data = request.json
        timetable.department = data['department']
        timetable.day = data['day']
        timetable.subject = data['subject']
        timetable.faculty_name = data['faculty_name']
        timetable.room_number = data['room_number']
        timetable.time_slot = data['time_slot']
        db.session.commit()
        return jsonify({'success': True, 'message': 'Timetable entry updated successfully'})
    
    elif request.method == 'DELETE':
        db.session.delete(timetable)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Timetable entry deleted successfully'})

# Initialize database
def create_tables():
    try:
        print(f"📁 Database path: {app.config['SQLALCHEMY_DATABASE_URI']}")
        db.create_all()
        print("✅ Database tables created/verified")
        
        # Create default admin user
        admin_exists = Admin.query.filter_by(username='admin').first()
        if not admin_exists:
            admin = Admin(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin user created")
        else:
            print("✅ Admin user already exists")
        
        # Add sample data
        block_count = Block.query.count()
        print(f"📊 Current block count: {block_count}")
        if block_count == 0:
            sample_blocks = [
                Block(name='AS Block', prefix='EW', description='Academic Sciences Block'),
                Block(name='IB Block', prefix='WW', description='Information Technology Block'),
                Block(name='SF Block', prefix='SF', description='Sunflower Block'),
                Block(name='Mechanical Block', prefix='ME', description='Mechanical Engineering Block'),
                Block(name='Research Park Block', prefix='AE', description='Aeronautical Engineering Block')
            ]
            for block in sample_blocks:
                db.session.add(block)
            db.session.commit()
            print(f"✅ Sample blocks added: {len(sample_blocks)} blocks")
        else:
            print(f"✅ Blocks already exist: {block_count} blocks")
            
        # Verify data
        final_block_count = Block.query.count()
        final_faculty_count = Faculty.query.count()
        final_timetable_count = Timetable.query.count()
        print(f"📊 Database status - Blocks: {final_block_count}, Faculty: {final_faculty_count}, Timetable: {final_timetable_count}")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()

# Initialize database on app startup (works for both direct run and WSGI servers)
with app.app_context():
    create_tables()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
