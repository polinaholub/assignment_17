import psycopg2
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker

# Add models for student, subject, and student_subject from previous lessons in SQLAlchemy.
# Find all students' names that visited 'English' classes.

connection = psycopg2.connect(
    host='localhost',
    database='postgres',
    user='postgres',
    password='password',
    port=5432,
)

query = '''CREATE TABLE
    student_subject (id serial PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student (id), FOREIGN KEY(subject_id) REFERENCES subject (id));'''

cursor = connection.cursor()
with connection.cursor() as curs:
    curs.execute("CREATE TABLE student (id serial PRIMARY KEY, name VARCHAR(100) NOT NULL, age INT NOT NULL)")
    curs.execute("CREATE TABLE subject (id serial PRIMARY KEY, name VARCHAR(150) NOT NULL)")
    curs.execute(query)
    curs.execute("INSERT INTO student (name, age) VALUES ('Bae', 18), ('Eddy', 21), ('Lily', 22), ('Jenny', 19);")
    curs.execute("INSERT INTO student_subject (student_id, subject_id) VALUES (1, 1), (2, 2), (3, 3), (4, 4), (1, 3);")

Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class StudentSubject(Base):
    __tablename__ = 'student_subject'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))

DATABASE_URI = 'postgresql://postgres:password@localhost:5432/postgres'

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

english = session.query(Subject).filter_by(name='English').first()
english_student_ids = session.query(StudentSubject).filter_by(subject_id=english.id).order_by(StudentSubject.student_id.asc()).all()
english_student_names = session.query(Student).filter(Student.id.in_([student.student_id for student in english_student_ids])).order_by(Student.name.asc()).all()

for student in english_student_names:
    print(student.name)