from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
import sqlite3


class Student(BaseModel):
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    age: Optional[int] = None
    major: Optional[str] = Field(max_length=20, default=None)


def create_table(filename: str):

    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS student (id INT, firstname TEXT, lastname TEXT, age INT, major TEXT, PRIMARY KEY(id))
        '''
    )
    conn.commit()

    cur.close()
    conn.close()


def db_add_student_(filename: str, student_id: int, student: Student):

    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    cur.execute(
        '''
        INSERT INTO STUDENT VALUES(?, ?, ?, ?, ?)
        ''',
        (student_id, student.first_name, student.last_name, student.age, student.major)
    )
    conn.commit()

    cur.close()
    conn.close()


def db_get_students(filename: str):

    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    cur.execute(
        '''
        SELECT * FROM student
        '''
    )
    conn.commit()

    students = cur.fetchall()

    cur.close()
    conn.close()

    return students


def db_delete_student(filename: str, student_id: int):

    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    cur.execute(
        '''
        DELETE FROM student
        WHERE id = ?
        ''',
        (student_id,)
    )
    conn.commit()

    cur.close()
    conn.close()


DATABASE = 'database.db'
app = FastAPI()
create_table(DATABASE)


@app.get('/', response_class=HTMLResponse)
def root():

    html_content = '''
    <div>Test!</div>
    '''
    return HTMLResponse(content=html_content, status_code=200)


@app.post('/student/{student_id}')
def add_student(student_id: int, student: Student):
    db_add_student_(DATABASE, student_id, student)
    return {'Status': 'Student added!'}


@app.get('/student')
def get_students():

    students = db_get_students(DATABASE)
    return students


@app.delete('/student/{student_id}')
def delete_student(student_id: int):
    db_delete_student(DATABASE, student_id)

    return db_get_students(DATABASE)
