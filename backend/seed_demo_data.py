from app.core.database import SessionLocal, engine
from app.core.security import hash_password
from app.models.base import Base
from app.models import (
    AcademicianProfile,
    Assessment,
    AssessmentAnswer,
    AssessmentAttempt,
    AssessmentQuestion,
    CompanyProfile,
    IndustryProfile,
    InstitutionProfile,
    Opportunity,
    QuestionOption,
    Skill,
    StudentProfile,
    User,
)


def seed_data():
    # Ensure all tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    universal_password = hash_password("Password123!")

    try:
        print("\n--- Seeding PIXIE Role-Based Demo Dataset ---")

        # ----------------------------------------------------
        # 1. SEED STUDENTS (3 Students)
        # ----------------------------------------------------
        students_data = [
            {
                "email": "student@pixie.com",
                "full_name": "Alex Rivers",
                "phone": "9876543210",
                "college_name": "Apex Institute of Technology",
                "degree": "Bachelor of Technology",
                "branch": "Computer Science",
                "graduation_year": 2026,
                "career_goal": "Backend Software Engineer",
                "bio": "Passionate computer science student eager to build scalable web applications and microservices.",
            },
            {
                "email": "student2@pixie.com",
                "full_name": "Sarah Jenkins",
                "phone": "9876543211",
                "college_name": "Apex Institute of Technology",
                "degree": "Bachelor of Technology",
                "branch": "Information Technology",
                "graduation_year": 2026,
                "career_goal": "Cloud Solutions Architect",
                "bio": "Specializing in distributed systems, AWS deployments, and DevOps automation.",
            },
            {
                "email": "student3@pixie.com",
                "full_name": "Rohan Verma",
                "phone": "9876543212",
                "college_name": "National Institute of Engineering",
                "degree": "Bachelor of Science",
                "branch": "Data Science",
                "graduation_year": 2027,
                "career_goal": "Machine Learning Engineer",
                "bio": "Enthusiastic about data algorithms, neural networks, and applied AI modeling.",
            },
        ]

        student_objs = []
        for s_data in students_data:
            user = db.query(User).filter(User.email == s_data["email"]).first()
            if not user:
                user = User(
                    email=s_data["email"],
                    password_hash=universal_password,
                    role="student",
                    is_active=True,
                    is_verified=True,
                )
                db.add(user)
                db.flush()
                print(f"Created Student User: {user.email} (ID: {user.id})")
            else:
                user.password_hash = universal_password
                user.role = "student"
                user.is_active = True
                db.flush()

            profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
            if not profile:
                profile = StudentProfile(
                    user_id=user.id,
                    full_name=s_data["full_name"],
                    phone=s_data["phone"],
                    college_name=s_data["college_name"],
                    degree=s_data["degree"],
                    branch=s_data["branch"],
                    graduation_year=s_data["graduation_year"],
                    career_goal=s_data["career_goal"],
                    bio=s_data["bio"],
                )
                db.add(profile)
                db.flush()
                print(f"Created StudentProfile: {profile.full_name} (Profile ID: {profile.id})")
            student_objs.append((user, profile))

        # ----------------------------------------------------
        # 2. SEED COMPANIES (2 Companies)
        # ----------------------------------------------------
        companies_data = [
            {
                "email": "techcorp@pixie.com",
                "company_name": "TechCorp Global",
                "industry": "Software & Cloud Systems",
                "website": "https://techcorp-global.example",
                "contact_person": "Vikram Malhotra (Director of Talent)",
                "phone": "9123456780",
                "location": "Bangalore & Remote",
                "description": "Global enterprise cloud and AI solutions provider partnering with leading academic institutions.",
            },
            {
                "email": "innovate@pixie.com",
                "company_name": "Innovate AI Labs",
                "industry": "Artificial Intelligence & Data",
                "website": "https://innovate-ai.example",
                "contact_person": "Elena Rostova (Head of University Relations)",
                "phone": "9123456781",
                "location": "Hyderabad & Hybrid",
                "description": "High-growth tech studio building intelligent next-generation platforms and analytics engines.",
            },
        ]

        industry_profile_objs = []
        for c_data in companies_data:
            user = db.query(User).filter(User.email == c_data["email"]).first()
            if not user:
                user = User(
                    email=c_data["email"],
                    password_hash=universal_password,
                    role="company",
                    is_active=True,
                    is_verified=True,
                )
                db.add(user)
                db.flush()
                print(f"Created Company User: {user.email} (ID: {user.id})")
            else:
                user.password_hash = universal_password
                user.role = "company"
                user.is_active = True
                db.flush()

            # Seed CompanyProfile
            c_profile = db.query(CompanyProfile).filter(CompanyProfile.user_id == user.id).first()
            if not c_profile:
                c_profile = CompanyProfile(
                    user_id=user.id,
                    company_name=c_data["company_name"],
                    phone=c_data["phone"],
                    industry=c_data["industry"],
                    website=c_data["website"],
                    contact_person=c_data["contact_person"],
                    location=c_data["location"],
                    description=c_data["description"],
                )
                db.add(c_profile)
                db.flush()

            # Also seed IndustryProfile for opportunities FK
            ind_profile = db.query(IndustryProfile).filter(IndustryProfile.user_id == user.id).first()
            if not ind_profile:
                ind_profile = IndustryProfile(
                    user_id=user.id,
                    company_name=c_data["company_name"],
                    industry_type=c_data["industry"],
                    website=c_data["website"],
                    location=c_data["location"],
                    description=c_data["description"],
                    is_verified=True,
                )
                db.add(ind_profile)
                db.flush()
            industry_profile_objs.append(ind_profile)

        # ----------------------------------------------------
        # 3. SEED INSTITUTIONS (1 Institution)
        # ----------------------------------------------------
        inst_data = {
            "email": "apex.institute@pixie.com",
            "institution_name": "Apex Institute of Technology",
            "phone": "9112233440",
            "institution_type": "Autonomous University",
            "location": "Pune, Maharashtra",
            "contact_person": "Dr. Suresh Kulkarni (Dean of Academics)",
            "website": "https://apex-institute.example",
            "description": "Premier engineering and research university focused on industry-aligned pedagogy and skills certification.",
        }

        user = db.query(User).filter(User.email == inst_data["email"]).first()
        if not user:
            user = User(
                email=inst_data["email"],
                password_hash=universal_password,
                role="institution",
                is_active=True,
                is_verified=True,
            )
            db.add(user)
            db.flush()
            print(f"Created Institution User: {user.email} (ID: {user.id})")
        else:
            user.password_hash = universal_password
            user.role = "institution"
            user.is_active = True
            db.flush()

        inst_profile = db.query(InstitutionProfile).filter(InstitutionProfile.user_id == user.id).first()
        if not inst_profile:
            inst_profile = InstitutionProfile(
                user_id=user.id,
                institution_name=inst_data["institution_name"],
                phone=inst_data["phone"],
                institution_type=inst_data["institution_type"],
                location=inst_data["location"],
                contact_person=inst_data["contact_person"],
                website=inst_data["website"],
                description=inst_data["description"],
            )
            db.add(inst_profile)
            db.flush()
            print(f"Created InstitutionProfile: {inst_profile.institution_name}")

        # ----------------------------------------------------
        # 4. SEED ACADEMICIANS (2 Academicians)
        # ----------------------------------------------------
        academicians_data = [
            {
                "email": "prof.sharma@pixie.com",
                "full_name": "Dr. Rajesh Sharma",
                "phone": "9887766550",
                "institution_name": "Apex Institute of Technology",
                "department": "Computer Science & Engineering",
                "designation": "Professor & Head of Department",
                "bio": "20+ years researching distributed algorithms, compiler design, and curriculum engineering.",
            },
            {
                "email": "prof.patel@pixie.com",
                "full_name": "Dr. Ananya Patel",
                "phone": "9887766551",
                "institution_name": "Apex Institute of Technology",
                "department": "Information Technology",
                "designation": "Associate Professor & Assessment Lead",
                "bio": "Specializes in software quality assurance, cloud architecture, and industry competency testing.",
            },
        ]

        for a_data in academicians_data:
            user = db.query(User).filter(User.email == a_data["email"]).first()
            if not user:
                user = User(
                    email=a_data["email"],
                    password_hash=universal_password,
                    role="academician",
                    is_active=True,
                    is_verified=True,
                )
                db.add(user)
                db.flush()
                print(f"Created Academician User: {user.email} (ID: {user.id})")
            else:
                user.password_hash = universal_password
                user.role = "academician"
                user.is_active = True
                db.flush()

            acad_profile = db.query(AcademicianProfile).filter(AcademicianProfile.user_id == user.id).first()
            if not acad_profile:
                acad_profile = AcademicianProfile(
                    user_id=user.id,
                    full_name=a_data["full_name"],
                    phone=a_data["phone"],
                    institution_name=a_data["institution_name"],
                    department=a_data["department"],
                    designation=a_data["designation"],
                    bio=a_data["bio"],
                )
                db.add(acad_profile)
                db.flush()
                print(f"Created AcademicianProfile: {acad_profile.full_name}")

        # ----------------------------------------------------
        # 5. SEED SKILLS & ASSESSMENTS (2 Skills & Assessments)
        # ----------------------------------------------------
        skill_python = db.query(Skill).filter(Skill.name == "Python Programming").first()
        if not skill_python:
            skill_python = Skill(
                name="Python Programming",
                category="Programming",
                description="Core Python programming language, data structures, and algorithmic logic.",
                is_active=True,
            )
            db.add(skill_python)
            db.flush()

        skill_cloud = db.query(Skill).filter(Skill.name == "Cloud Computing & DevOps").first()
        if not skill_cloud:
            skill_cloud = Skill(
                name="Cloud Computing & DevOps",
                category="Infrastructure",
                description="Cloud architecture patterns, containerization, and modern deployment models.",
                is_active=True,
            )
            db.add(skill_cloud)
            db.flush()

        # Assessment 1: Python
        assessment1 = db.query(Assessment).filter(Assessment.title == "Python Foundations Assessment").first()
        if not assessment1:
            assessment1 = Assessment(
                skill_id=skill_python.id,
                title="Python Foundations Assessment",
                description="Fundamental concepts of Python including data types, functions, and OOP principles.",
                difficulty="beginner",
                time_limit_minutes=15,
                is_active=True,
            )
            db.add(assessment1)
            db.flush()

        # Assessment 2: Cloud Computing
        assessment2 = db.query(Assessment).filter(Assessment.title == "Cloud & DevOps Essentials").first()
        if not assessment2:
            assessment2 = Assessment(
                skill_id=skill_cloud.id,
                title="Cloud & DevOps Essentials",
                description="Comprehensive evaluation of microservices, virtualization, containerization, and CI/CD.",
                difficulty="intermediate",
                time_limit_minutes=20,
                is_active=True,
            )
            db.add(assessment2)
            db.flush()

        # Questions for Assessment 1 (Python)
        q1_data = [
            {
                "text": "What is the output of print(type([])) in Python?",
                "opts": [
                    ("<class 'list'>", True),
                    ("<class 'array'>", False),
                    ("<class 'set'>", False),
                    ("<class 'tuple'>", False),
                ],
            },
            {
                "text": "Which keyword is used to define a function in Python?",
                "opts": [
                    ("func", False),
                    ("def", True),
                    ("function", False),
                    ("lambda", False),
                ],
            },
            {
                "text": "Which of the following data structures in Python is immutable?",
                "opts": [
                    ("list", False),
                    ("dict", False),
                    ("tuple", True),
                    ("set", False),
                ],
            },
        ]

        for idx, item in enumerate(q1_data, 1):
            q = db.query(AssessmentQuestion).filter(
                AssessmentQuestion.assessment_id == assessment1.id,
                AssessmentQuestion.question_text == item["text"],
            ).first()
            if not q:
                q = AssessmentQuestion(
                    assessment_id=assessment1.id,
                    question_text=item["text"],
                    question_type="mcq",
                    difficulty="beginner",
                    marks=1,
                    order_index=idx,
                )
                db.add(q)
                db.flush()
                for o_idx, (opt_text, is_c) in enumerate(item["opts"], 1):
                    db.add(QuestionOption(
                        question_id=q.id,
                        option_text=opt_text,
                        is_correct=is_c,
                        order_index=o_idx,
                    ))

        # Questions for Assessment 2 (Cloud)
        q2_data = [
            {
                "text": "Which cloud computing model offers on-demand computing resources like VMs, storage, and networking?",
                "opts": [
                    ("IaaS (Infrastructure as a Service)", True),
                    ("PaaS (Platform as a Service)", False),
                    ("SaaS (Software as a Service)", False),
                    ("FaaS (Function as a Service)", False),
                ],
            },
            {
                "text": "In Docker containerization, which file defines the instructions for assembling a container image?",
                "opts": [
                    ("docker-compose.yml", False),
                    ("Dockerfile", True),
                    ("Containerfile.lock", False),
                    ("config.json", False),
                ],
            },
            {
                "text": "Which HTTP status code signifies a resource was successfully created on the server?",
                "opts": [
                    ("200 OK", False),
                    ("201 Created", True),
                    ("204 No Content", False),
                    ("202 Accepted", False),
                ],
            },
        ]

        for idx, item in enumerate(q2_data, 1):
            q = db.query(AssessmentQuestion).filter(
                AssessmentQuestion.assessment_id == assessment2.id,
                AssessmentQuestion.question_text == item["text"],
            ).first()
            if not q:
                q = AssessmentQuestion(
                    assessment_id=assessment2.id,
                    question_text=item["text"],
                    question_type="mcq",
                    difficulty="intermediate",
                    marks=1,
                    order_index=idx,
                )
                db.add(q)
                db.flush()
                for o_idx, (opt_text, is_c) in enumerate(item["opts"], 1):
                    db.add(QuestionOption(
                        question_id=q.id,
                        option_text=opt_text,
                        is_correct=is_c,
                        order_index=o_idx,
                    ))

        # ----------------------------------------------------
        # 6. SEED OPPORTUNITIES (3 Real Opportunities)
        # ----------------------------------------------------
        if industry_profile_objs:
            primary_ind = industry_profile_objs[0]
            opps_data = [
                {
                    "title": "Backend Engineering Intern",
                    "opportunity_type": "Internship",
                    "description": "Build high-throughput APIs using FastAPI, PostgreSQL, and Redis caching. Work closely with Senior Cloud Engineers.",
                    "location": "Bangalore (Hybrid)",
                    "work_mode": "Hybrid",
                    "duration": "6 Months",
                    "stipend": 35000,
                    "experience_required": "0-1 Years",
                    "eligibility": "B.Tech / B.Sc in Computer Science with verified Python skills.",
                },
                {
                    "title": "Cloud Infrastructure Associate",
                    "opportunity_type": "Full Time",
                    "description": "Design and maintain AWS Kubernetes clusters, CI/CD deployment pipelines, and observability telemetry.",
                    "location": "Remote",
                    "work_mode": "Remote",
                    "duration": "Full Time",
                    "stipend": 75000,
                    "experience_required": "Fresher / Final Year",
                    "eligibility": "Strong grounding in Linux, Docker, and Cloud architectures.",
                },
                {
                    "title": "AI / ML Research Fellow",
                    "opportunity_type": "Project Fellowship",
                    "description": "Collaborate with university researchers on LLM inference optimization, retrieval augmented generation, and vector embeddings.",
                    "location": "Hyderabad",
                    "work_mode": "In-Office",
                    "duration": "12 Months",
                    "stipend": 45000,
                    "experience_required": "Student / Researcher",
                    "eligibility": "Proficiency with Python, PyTorch, and linear algebra.",
                },
            ]

            for o_data in opps_data:
                existing_opp = db.query(Opportunity).filter(
                    Opportunity.title == o_data["title"],
                    Opportunity.industry_id == primary_ind.id,
                ).first()
                if not existing_opp:
                    new_opp = Opportunity(
                        industry_id=primary_ind.id,
                        title=o_data["title"],
                        opportunity_type=o_data["opportunity_type"],
                        description=o_data["description"],
                        location=o_data["location"],
                        work_mode=o_data["work_mode"],
                        duration=o_data["duration"],
                        stipend=o_data["stipend"],
                        experience_required=o_data["experience_required"],
                        eligibility=o_data["eligibility"],
                        is_active=True,
                    )
                    db.add(new_opp)
                    print(f"Created Opportunity: {new_opp.title}")

        db.commit()
        print("\n[SUCCESS] Seed Demo Data execution completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
