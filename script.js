// College Assistant Chatbot JavaScript

// JSON Data
const collegeData = {
    "college_name": "Your College Name",
    "blocks": [
        {"name": "AS BLOCK", "prefix": "EW"},
        {"name": "IB BLOCK", "prefix": "WW"},
        {"name": "SUNFLOWER (SF) BLOCK", "prefix": "SF"},
        {"name": "MECHANICAL BLOCK", "prefix": "ME"},
        {"name": "RESEARCH PARK BLOCK", "prefix": "AE"}
    ],
    "departments": [
        {
            "name": "Artificial Intelligence & Data Science",
            "code": "AIDS",
            "faculty": [
                {"name": "Dr Gomathi R", "designation": "Professor & Head", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Sundara Murthy S", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Eswaramoorthy V", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Arun Kumar R", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Nandhini S S", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Balasamy K", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Subbulakshmi M", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Ranjith G", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Prabanand S C", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Nithyapriya S", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Esakki Madura E", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Chozharajan P", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Nisha Devi K", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Raj Kumar V S", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Divyabarathi P", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Vaanathi S", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Satheeshkumar S", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Satheesh N P", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Kiruthiga R", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Ashforn Hermina J M", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Jeevitha S V", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Premkumar C", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Benita Gracia Thangam J", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Reshmi T S", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Kalpana R", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Suriya V", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Hema Priya D", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Priyadharshni S", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Manju M", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Sasson Taffwin Moses S", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Manochitra A S", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"}
            ]
        },
        {
            "name": "Computer Science & Engineering",
            "code": "CSE",
            "faculty": [
                {"name": "Dr Sasikala D", "designation": "Professor & Head", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Premalatha K", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Sathishkumar P", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Sangeethaa S N", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Rajeshkumar G", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Karthiga M", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Saranya K", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Deepa Priya B S", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Ramya R", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Parthasarathi P", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Dhivya P", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Rajesh Kanna P", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Praveen V", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Dinesh P S", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Ganagavalli K", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Swathypriyadharsini P", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Sathishkannan R", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Ramasami S", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Prabha Devi D", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Soundariya R S", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Suseendran S", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Ammu V", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Alamelu M", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Kavitha R", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Magesh Kumar B", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Kiruthika V R", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Nithya R", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Sangavi N", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Mohan Kumar V", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Chitradevi T N", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Gayathri S", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Kalaivani E", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Steephan Amalraj J", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Sathyamoorthy J", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Mohanambal K", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Gunavardini V", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Priyanga M A", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Sathiya B", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Rathna S", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Parkavi S", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Rangaraj K", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Mythili G M", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Gayathiri Devi S", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Kayalvizhi B", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Thangatamilselvi S", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Mahesh S", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Jackson J", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Aswin Jaya Surya M J", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"}
            ]
        },
        {
            "name": "Electronics & Communication Engineering",
            "code": "ECE",
            "faculty": [
                {"name": "Dr Prakash S P", "designation": "Head", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Harikumar R", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Poongodi C", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Sampoornam K P", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Perarasi T", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Sanjoy Deb", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Pushpavalli M", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Sannasi Chakravarthy S R", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Venkateshkumar U", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Sathiyamurthi P", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Ramya P", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Elango S", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Sajan P Philip", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Arulmurugan L", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Murugan K", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Daniel Raj A", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Kanthimathi N", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Leeban Moses M", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Ramkumar R", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Nirmal Kumar R", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Tamilselvan S", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Dhanalakshmi S", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Sankarananth S", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Karthikeyan S", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Saranya N", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Raja Sekar S", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Baranidharan V", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Stephen Sagayaraj A", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Vellingiri A", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Mythili S", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Pousia S", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Gayathri R", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Krishnaraj R", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Sharmila A", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Abinaya M", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Soundarya B", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Jeevitha R", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"}
            ]
        },
        {
            "name": "Mechanical Engineering",
            "code": "MECH",
            "faculty": [
                {"name": "Dr Ravi K", "designation": "Professor & Head", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Anitha R", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Sathish P", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Murugan S", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Arulmozhi R", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Karthikeyan M", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Ramesh P", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Selvakumar T", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Vijayakumar N", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Arulraj M", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Suresh R", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Gokul R", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Santhosh K", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Arunkumar P", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Senthilkumar R", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Balaji M", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Rajendran K", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Suresh Kumar P", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Nirmal S", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Vinoth P", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Prakash S", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Arun S", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Manikandan K", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"}
            ]
        },
        {
            "name": "Aeronautical Engineering",
            "code": "AE",
            "faculty": [
                {"name": "Dr Mohan R", "designation": "Professor & Head", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Sathish Kumar P", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Anitha S", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Gokul R", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Ravi K", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Selva P", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Arul P", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Balaji K", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Vinoth S", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Ramesh V", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"}
            ]
        },
        {
            "name": "Information Technology",
            "code": "IT",
            "faculty": [
                {"name": "Dr Sathishkumar S", "designation": "Professor & Head", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Ramya P", "designation": "Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Dr Anitha R", "designation": "Associate Professor", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Manoj K", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Kavitha S", "designation": "Assistant Professor Level III", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Selvi M", "designation": "Assistant Professor Level II", "phone": "RANDOM_7DIGIT_3XXX"},
                {"name": "Prof Divya R", "designation": "Assistant Professor", "phone": "RANDOM_7DIGIT_3XXX"}
            ]
        }
    ],
    "rules": {
        "classroom_mapping": "AS BLOCK = EW, IB BLOCK = WW, SF BLOCK = SF, MECHANICAL BLOCK = ME, RESEARCH PARK = AE",
        "timetable_generation": "Generate department-wise timetable dynamically on prompt request.",
        "faculty_phone_rule": "All faculty phones should be generated randomly as 7-digit numbers starting with 3XXX"
    }
};

// Utility Functions
function generateRandomPhone() {
    return '3' + Math.floor(Math.random() * 1000000).toString().padStart(6, '0');
}

function getCurrentTime() {
    return new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

function addMessage(content, isUser = false) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = isUser ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.innerHTML = content;
    
    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = getCurrentTime();
    
    messageContent.appendChild(messageText);
    messageContent.appendChild(messageTime);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.id = 'typingIndicator';
    
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-text">
                <div class="typing-indicator">
                    <span>Assistant is typing</span>
                    <div class="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Classroom Location Finder
function findClassroomLocation(classroomCode) {
    const blocks = collegeData.blocks;
    
    for (let block of blocks) {
        if (classroomCode.startsWith(block.prefix)) {
            return {
                found: true,
                block: block.name,
                classroom: classroomCode
            };
        }
    }
    
    return {
        found: false,
        classroom: classroomCode
    };
}

// Faculty Information Handler
function getFacultyInfo(departmentCode) {
    const department = collegeData.departments.find(dept => 
        dept.code.toLowerCase() === departmentCode.toLowerCase()
    );
    
    if (!department) {
        return null;
    }
    
    // Generate random phone numbers for faculty
    const facultyWithPhones = department.faculty.map(faculty => ({
        ...faculty,
        phone: generateRandomPhone()
    }));
    
    return {
        department: department.name,
        code: department.code,
        faculty: facultyWithPhones
    };
}

// Timetable Generator
function generateTimetable(departmentCode) {
    const department = collegeData.departments.find(dept => 
        dept.code.toLowerCase() === departmentCode.toLowerCase()
    );
    
    if (!department) {
        return null;
    }
    
    // Generate a sample timetable
    const timeSlots = ['9:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-1:00', '2:00-3:00', '3:00-4:00', '4:00-5:00'];
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
    const subjects = ['Data Structures', 'Algorithms', 'Database Systems', 'Web Development', 'Machine Learning', 'Software Engineering', 'Computer Networks'];
    const classrooms = ['EW201', 'EW202', 'EW203', 'WW101', 'WW102', 'SF301', 'SF302', 'ME401', 'AE501'];
    
    const timetable = [];
    
    for (let day of days) {
        const daySchedule = { day, classes: [] };
        
        for (let i = 0; i < timeSlots.length; i++) {
            const subject = subjects[Math.floor(Math.random() * subjects.length)];
            const faculty = department.faculty[Math.floor(Math.random() * department.faculty.length)];
            const classroom = classrooms[Math.floor(Math.random() * classrooms.length)];
            
            daySchedule.classes.push({
                time: timeSlots[i],
                subject: subject,
                faculty: faculty.name,
                classroom: classroom
            });
        }
        
        timetable.push(daySchedule);
    }
    
    return {
        department: department.name,
        code: department.code,
        timetable: timetable
    };
}

// Main Response Handler
function processUserInput(input) {
    const lowerInput = input.toLowerCase().trim();
    
    // Classroom location queries
    if (lowerInput.includes('where is') || lowerInput.includes('location of')) {
        const classroomMatch = input.match(/([A-Z]{2}\d{3})/);
        if (classroomMatch) {
            const classroomCode = classroomMatch[1];
            const result = findClassroomLocation(classroomCode);
            
            if (result.found) {
                return `
                    <div class="classroom-info">
                        <h3>📍 Classroom Location Found!</h3>
                        <p><strong>${result.classroom}</strong> is in <strong>${result.block}</strong></p>
                    </div>
                `;
            } else {
                return `
                    <div class="classroom-info" style="background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);">
                        <h3>❌ Classroom Not Found</h3>
                        <p>Sorry, I couldn't find information for <strong>${result.classroom}</strong></p>
                        <p>Please check the classroom code and try again.</p>
                    </div>
                `;
            }
        }
    }
    
    // Faculty information queries
    if (lowerInput.includes('faculty') || lowerInput.includes('staff') || lowerInput.includes('professor')) {
        const departmentCodes = ['aids', 'cse', 'ece', 'mech', 'ae', 'it'];
        let targetDept = null;
        
        for (let code of departmentCodes) {
            if (lowerInput.includes(code)) {
                targetDept = code;
                break;
            }
        }
        
        if (targetDept) {
            const facultyInfo = getFacultyInfo(targetDept);
            if (facultyInfo) {
                let tableHTML = `
                    <h3>👨‍🏫 ${facultyInfo.department} Faculty</h3>
                    <table class="faculty-table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Designation</th>
                                <th>Phone</th>
                            </tr>
                        </thead>
                        <tbody>
                `;
                
                facultyInfo.faculty.forEach(faculty => {
                    tableHTML += `
                        <tr>
                            <td>${faculty.name}</td>
                            <td>${faculty.designation}</td>
                            <td>${faculty.phone}</td>
                        </tr>
                    `;
                });
                
                tableHTML += `
                        </tbody>
                    </table>
                `;
                
                return tableHTML;
            }
        }
    }
    
    // Timetable queries
    if (lowerInput.includes('timetable') || lowerInput.includes('schedule')) {
        const departmentCodes = ['aids', 'cse', 'ece', 'mech', 'ae', 'it'];
        let targetDept = null;
        
        for (let code of departmentCodes) {
            if (lowerInput.includes(code)) {
                targetDept = code;
                break;
            }
        }
        
        if (targetDept) {
            const timetable = generateTimetable(targetDept);
            if (timetable) {
                let tableHTML = `
                    <h3>📅 ${timetable.department} Timetable</h3>
                    <table class="timetable">
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Monday</th>
                                <th>Tuesday</th>
                                <th>Wednesday</th>
                                <th>Thursday</th>
                                <th>Friday</th>
                            </tr>
                        </thead>
                        <tbody>
                `;
                
                const timeSlots = ['9:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-1:00', '2:00-3:00', '3:00-4:00', '4:00-5:00'];
                
                for (let i = 0; i < timeSlots.length; i++) {
                    tableHTML += '<tr>';
                    tableHTML += `<td class="time-slot">${timeSlots[i]}</td>`;
                    
                    for (let day of timetable.timetable) {
                        const classInfo = day.classes[i];
                        tableHTML += `
                            <td>
                                <strong>${classInfo.subject}</strong><br>
                                <small>${classInfo.faculty}</small><br>
                                <small>${classInfo.classroom}</small>
                            </td>
                        `;
                    }
                    
                    tableHTML += '</tr>';
                }
                
                tableHTML += `
                        </tbody>
                    </table>
                `;
                
                return tableHTML;
            }
        }
    }
    
    // Default response
    return `
        <p>I can help you with:</p>
        <ul>
            <li>📍 <strong>Classroom Locations:</strong> Ask "Where is EW201?" or "Location of WW102"</li>
            <li>👨‍🏫 <strong>Faculty Information:</strong> Ask "Show AIDS faculty" or "CSE staff"</li>
            <li>📅 <strong>Timetables:</strong> Ask "Generate CSE timetable" or "AIDS schedule"</li>
        </ul>
        <p>Try asking me something specific!</p>
    `;
}

// Event Handlers
function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (message === '') return;
    
    // Add user message
    addMessage(message, true);
    
    // Clear input
    userInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Process response after a short delay
    setTimeout(() => {
        hideTypingIndicator();
        const response = processUserInput(message);
        addMessage(response);
    }, 1500);
}

function askQuestion(question) {
    document.getElementById('userInput').value = question;
    sendMessage();
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    
    // Add event listeners
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    sendBtn.addEventListener('click', sendMessage);
    
    // Focus on input
    userInput.focus();
});
