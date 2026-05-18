"""
Sample Resume Data for Testing
Production-level AI ATS Resume Screening Platform
"""

SAMPLE_RESUMES = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@email.com",
        "phone": "+1-415-555-0101",
        "resume_text": """
        ALICE JOHNSON
        San Francisco, CA | (415) 555-0101 | alice.johnson@email.com | LinkedIn.com/in/alicejohnson
        
        PROFESSIONAL SUMMARY
        Senior Software Engineer with 8+ years of experience developing scalable web applications and cloud infrastructure. 
        Expertise in Python, JavaScript, React, AWS, and Docker. Proven track record of leading cross-functional teams 
        and delivering projects on time.
        
        TECHNICAL SKILLS
        Languages: Python, JavaScript, TypeScript, SQL, Bash
        Frameworks: React, Django, Flask, Spring Boot
        Cloud Platforms: AWS (EC2, S3, Lambda, RDS), Azure, GCP
        Tools & Technologies: Docker, Kubernetes, Jenkins, Git, JIRA
        Databases: PostgreSQL, MongoDB, Redis, Elasticsearch
        
        PROFESSIONAL EXPERIENCE
        
        Senior Software Engineer | TechCorp Inc. | San Francisco, CA | 2021 - Present
        • Led development of microservices architecture, reducing deployment time by 60%
        • Mentored team of 5 junior developers, improving code quality metrics by 35%
        • Designed and implemented CI/CD pipeline using Jenkins and Docker
        • Optimized database queries, reducing API response time from 2s to 200ms
        
        Software Engineer | DataSystems Ltd. | San Francisco, CA | 2018 - 2021
        • Developed full-stack web applications using Python, React, and PostgreSQL
        • Implemented AWS Lambda functions for real-time data processing
        • Built REST APIs serving 1M+ daily requests with 99.9% uptime
        • Collaborated with product team to deliver features on schedule
        
        Junior Developer | StartUp XYZ | San Francisco, CA | 2016 - 2018
        • Developed features for customer-facing web application
        • Participated in code reviews and testing processes
        
        EDUCATION
        Bachelor of Science in Computer Science | Stanford University | 2016
        GPA: 3.8/4.0
        
        CERTIFICATIONS
        • AWS Certified Solutions Architect - Professional (2022)
        • Google Cloud Professional Data Engineer (2021)
        
        PROJECTS
        • Built E-commerce Platform: Developed full-stack platform handling $5M+ annual transactions
        • Real-time Analytics Dashboard: Created dashboard processing 100k events per second
        
        ACHIEVEMENTS
        • Employee of the Year (2022)
        • Published 3 technical articles on Medium with 50k+ views
        """
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob.smith@email.com",
        "phone": "+1-917-555-0202",
        "resume_text": """
        BOB SMITH
        New York, NY | (917) 555-0202 | bob.smith@email.com | GitHub.com/bobsmith
        
        OBJECTIVE
        Experienced Full Stack Developer seeking challenging position to leverage expertise in web development 
        and cloud technologies.
        
        CORE COMPETENCIES
        • Full Stack Web Development (Frontend & Backend)
        • Python, JavaScript, React
        • AWS Services & Cloud Architecture
        • Database Design & Optimization
        • Problem Solving & System Design
        
        CAREER HISTORY
        
        Full Stack Developer | CloudTech Solutions | New York, NY | 2019 - Present
        • Developed React-based user interface for data analytics platform
        • Created Python backend services using Flask and PostgreSQL
        • Managed AWS infrastructure including EC2, S3, and RDS
        • Implemented automated testing with 85% code coverage
        
        Software Developer | WebServices Co. | New York, NY | 2017 - 2019
        • Built features for SaaS platform using JavaScript and Node.js
        • Worked with MongoDB and Redis for data storage
        • Participated in agile development process
        
        EDUCATION
        Bachelor of Science in Information Technology | New York University | 2017
        
        TECHNICAL SKILLS
        Programming: Python, JavaScript, HTML, CSS
        Frameworks: React, Flask, Express.js
        Databases: PostgreSQL, MongoDB
        Cloud: AWS, Docker, Git
        
        ADDITIONAL CERTIFICATIONS
        • AWS Certified Developer (2021)
        """
    },
    {
        "id": 3,
        "name": "Carol Davis",
        "email": "carol.davis@email.com",
        "phone": "+1-310-555-0303",
        "resume_text": """
        CAROL DAVIS
        Los Angeles, CA | carol.davis@email.com | (310) 555-0303 | linkedin.com/in/caroldavis
        
        SUMMARY
        Data Engineer with 6 years of experience building scalable data pipelines and data warehouses. 
        Strong background in Python, SQL, and big data technologies.
        
        SKILLS
        Programming Languages: Python, SQL, Scala, Bash
        Big Data: Spark, Hadoop, Kafka, Airflow
        Databases: PostgreSQL, Snowflake, Redshift, BigQuery
        Cloud Platforms: AWS (S3, EC2, Lambda), Google Cloud Platform
        Tools: Git, Docker, Tableau
        
        WORK EXPERIENCE
        
        Senior Data Engineer | DataCorp Analytics | Los Angeles, CA | 2020 - Present
        • Designed and built data pipelines processing 10TB+ data daily
        • Optimized Spark jobs reducing processing time by 40%
        • Implemented data quality checks and monitoring systems
        • Led implementation of data warehouse on Snowflake
        
        Data Engineer | InfoSystems Inc. | Los Angeles, CA | 2018 - 2020
        • Developed ETL pipelines using Python and Apache Spark
        • Created analytical dashboards using Tableau
        • Managed AWS infrastructure for data processing
        
        Junior Data Analyst | Analytics Startup | Los Angeles, CA | 2017 - 2018
        • Analyzed data and created reports
        • Developed SQL queries for business intelligence
        
        EDUCATION
        Master of Science in Data Science | UC Berkeley | 2017
        Bachelor of Science in Mathematics | UCLA | 2015
        
        CERTIFICATIONS
        Google Cloud Professional Data Engineer (2021)
        Databricks Certified Associate Data Engineer
        """
    }
]

SAMPLE_JOB_DESCRIPTION = """
Position: Senior Full Stack Developer

Company: TechVenture Inc.
Location: San Francisco, CA (Remote)
Experience Required: 5+ years

About Us:
We are a fast-growing technology company revolutionizing the software industry with AI-powered solutions.

Job Description:
We are looking for a Senior Full Stack Developer to join our engineering team. You will be responsible for 
designing and developing scalable web applications and cloud infrastructure.

Key Responsibilities:
• Design and develop full-stack web applications
• Build and maintain microservices architecture
• Collaborate with cross-functional teams
• Mentor junior developers
• Implement CI/CD pipelines
• Optimize application performance

Required Skills:
• 5+ years of software development experience
• Expert level in Python or Java
• Strong JavaScript/React experience
• AWS or Azure cloud platform experience
• Docker and Kubernetes knowledge
• SQL and NoSQL databases
• Git version control
• Strong communication skills

Nice to Have:
• Machine learning experience
• Leadership experience
• Published technical articles
• Open source contributions

Benefits:
• Competitive salary
• Stock options
• Health insurance
• Remote work flexibility
• Professional development budget
"""

# Skills database for testing
REQUIRED_SKILLS = [
    "Python",
    "JavaScript",
    "React",
    "AWS",
    "Docker",
    "SQL",
    "Java",
    "Communication",
    "Problem Solving",
    "Leadership"
]
