##################
#프로그램명: 성적 관리 프로그램
#작성자: 소프트웨어학부/전성현
#작성일: 2025/05/29
#프로그램 설명: 학번, 이름, 영어점수, C-언어 점수, 파이썬 점수를 입력받아 총점, 평균, 학점, 등수를 계산하여 MySQL 데이터베이스에 저장하는 프로그램입니다. 
###################
import pymysql

db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='tjs3568178!',
    db='managescore',
    charset='utf8'
)

cursor = db.cursor()

class Student:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.scores = {"영어":0, "C언어":0, "파이썬":0}
        self.total = 0
        self.average = 0.0
        self.grade = ''
        self.rank = 0

    # 점수 입력 및 총합, 평균, 학점 계산해서 저장
    def input_scores(self, subjects):
        # 과목 별 점수 입력
        for subject in subjects:
            self.scores[subject] = int(input(f"{self.name} 학생의 {subject} 점수 : "))
        #총합 계산
        self.total = sum(self.scores.values())
        #평균 계산
        self.average = self.total / len(subjects)
        #학점 계산
        self.grade = self.get_grade()
    
    def get_grade(self):
        if self.average >= 90: # 90점 이상이면 A
            return 'A'
        elif self.average >= 80: # 80점 이상이면 B
            return 'B'
        elif self.average >= 70: # 70점 이상이면 C
            return 'C'
        elif self.average >= 60: # 60점 이상면 D
            return 'D'
        else: #60점 미만이면 F
            return 'F'

create_students_sql = """
CREATE TABLE IF NOT EXISTS students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    number INT UNIQUE NOT NULL,
    total INT DEFAULT 0,
    average DECIMAL(5,2) DEFAULT 0.00,
    grade CHAR(1) DEFAULT '',
    `rank` INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_scores_sql = """
CREATE TABLE IF NOT EXISTS scores (
    score_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    subject VARCHAR(20) NOT NULL,
    score INT CHECK (score >= 0 AND score <= 100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);
"""

#시작 메뉴 그리는 함수
def drawStartMenu():
    print('-'*60)
    print("\n학생 성적 입력 프로그램\n")
    print('-'*60)
    print("1. 학생 정보 및 성적 입력\n")
    print("2. 학생 정보 삭제\n")
    print("3. 학생 정보 검색 및 성적 조회(학번, 이름)\n")
    print("4. 전체 학생 성적 조회\n")
    print("5. 종료\n")

#학생 성적 조회 메뉴 그리는 함수
def drawMiniMenu():
    print("\n학생 성적 결과\n")
    print('-'*60)
    print("이름\t영어\tC언어\t파이썬\t총점\t평균\t학점\t등수")
    print('-'*60)

# 학생 등수 계산 함수
def rankStudent(students):
    total_scores = [student.total for student in students.values()]
    sorted_scores = sorted(total_scores, reverse=True)
    for student in students.values():
        student.rank = sorted_scores.index(student.total) + 1 

# 데이터베이스 등수 업데이트 함수
def updateAllRanksInDB():
    cursor.execute("SET @rank = 0;")
    rank_update_sql = """
        UPDATE students 
        SET `rank` = (@rank := @rank + 1)
        ORDER BY total DESC;
        """
    cursor.execute(rank_update_sql)

#학생 객체 생성 및 성적 입력 함수
def inputStudentData(students, subjects):
    cursor.execute("SELECT COUNT(*) FROM students;")
    db_count = cursor.fetchone()[0]
    
    if db_count >= 5:
        print("더 이상 입력할 수 없습니다.")
    else:
        name = input("학생 이름 입력: ")
        number = int(input("학생 학번 입력: "))
        
        check_sql = "SELECT COUNT(*) FROM students WHERE name = %s OR number = %s;"
        cursor.execute(check_sql, (name, number))
        if cursor.fetchone()[0] > 0:
            print("이미 존재하는 학생 이름 또는 학번입니다.")
            return
        
        students[name] = Student(name, number)
        students[name].input_scores(subjects)
        rankStudent(students)
        
        default = """
        INSERT INTO students (name, number, total, average, grade, `rank`) VALUES (%s, %s, %s, %s, %s, %s);
        """
        score_sql = """
        INSERT INTO scores (student_id, subject, score) VALUES (%s, %s, %s);
        """

        cursor.execute(default, (name, number, students[name].total, students[name].average, students[name].grade, students[name].rank))

        student_id = cursor.lastrowid

        for subject, score_value in students[name].scores.items():
            cursor.execute(score_sql, (student_id, subject, score_value))
        
        updateAllRanksInDB()
        db.commit()

        print("입력 완료!")

#학생 삭제 함수    
def deleteStudentData():
    name = input("삭제할 학생 이름 입력: ")
    stdNumber = int(input("학생 학번 입력: "))
    
    check_sql = """
    SELECT student_id FROM students WHERE name = %s AND number = %s;
    """
    cursor.execute(check_sql, (name, stdNumber))
    student = cursor.fetchone()

    if student:
        student_id = student[0]
        print(f"{name} 학생을 삭제합니다.\n")
   
        delete_sql = """
        DELETE FROM students WHERE student_id = %s;
        """
        cursor.execute(delete_sql, (student_id,))
   
        updateAllRanksInDB()
        db.commit()
        print("학생 삭제 및 등수 업데이트 완료!")
    
    else:
        print(f"학생 이름 또는 학번이 잘못되었습니다.\n")

#학생 검색 함수
def searchStudentData():
    name = input("검색할 학생 이름 입력: ")
    stdNumber = int(input("검색할 학생 학번 입력: "))
    
    student_sql = """
        SELECT student_id, name, number, total, average, grade, `rank` 
        FROM students 
        WHERE name = %s AND number = %s;
        """
    cursor.execute(student_sql, (name, stdNumber))
    student = cursor.fetchone()
   
    if student:
        student_id, name, number, total, average, grade, rank = student
        print(f"{number}의 {name} 학생이 존재합니다.\n")
       
        scores_sql = """
            SELECT subject, score 
            FROM scores 
            WHERE student_id = %s 
            ORDER BY subject;
            """
        cursor.execute(scores_sql, (student_id,))
        scores_data = cursor.fetchall()
       
        scores = {subject: score for subject, score in scores_data}
       
        drawMiniMenu()
        print(f"{name}\t{scores.get('영어', 0)}\t{scores.get('C언어', 0)}\t{scores.get('파이썬', 0)}\t"
             f"{total}\t{average:.2f}\t{grade}\t{rank}")
    else:
        print(f"학생 이름 또는 학번이 잘못되었습니다.\n")

#전체 학생 성적 조회 함수
def showAllStudentGrade():
    count_sql = """
        SELECT COUNT(*) FROM students WHERE average >= 80.0;
        """
    cursor.execute(count_sql)
    n = cursor.fetchone()[0]

    c = input("총점 기준으로 학생들을 정렬하시겠습니까?(Y/N) : ")
    
    if c == 'Y':
        sorted_sql = """
            SELECT s.name, s.total, s.average, s.grade, s.rank,
                   MAX(CASE WHEN sc.subject = '영어' THEN sc.score END) as 영어,
                   MAX(CASE WHEN sc.subject = 'C언어' THEN sc.score END) as C언어,
                   MAX(CASE WHEN sc.subject = '파이썬' THEN sc.score END) as 파이썬
            FROM students s
            LEFT JOIN scores sc ON s.student_id = sc.student_id
            GROUP BY s.student_id, s.name, s.total, s.average, s.grade, s.rank
            ORDER BY s.total DESC;
            """
        cursor.execute(sorted_sql)
        students_data = cursor.fetchall()
        
        drawMiniMenu()
        for student in students_data:
            name, total, average, grade, rank, eng, c_lang, python = student
            print(f"{name}\t{eng or 0}\t{c_lang or 0}\t{python or 0}\t"
                  f"{total}\t{average:.2f}\t{grade}\t{rank}")
        print(f"80점 이상인 학생 수 : {n}")

    else:
        normal_sql = """
            SELECT s.name, s.total, s.average, s.grade, s.rank,
                   MAX(CASE WHEN sc.subject = '영어' THEN sc.score END) as 영어,
                   MAX(CASE WHEN sc.subject = 'C언어' THEN sc.score END) as C언어,
                   MAX(CASE WHEN sc.subject = '파이썬' THEN sc.score END) as 파이썬
            FROM students s
            LEFT JOIN scores sc ON s.student_id = sc.student_id
            GROUP BY s.student_id, s.name, s.total, s.average, s.grade, s.rank;
            """
        cursor.execute(normal_sql)
        students_data = cursor.fetchall()
        
        drawMiniMenu()
        for student in students_data:
            name, total, average, grade, rank, eng, c_lang, python = student
            print(f"{name}\t{eng or 0}\t{c_lang or 0}\t{python or 0}\t"
                  f"{total}\t{average:.2f}\t{grade}\t{rank}")
        print(f"80점 이상인 학생 수 : {n}")

# 테이블 생성
cursor.execute(create_students_sql)
cursor.execute(create_scores_sql)
db.commit()
print("테이블 생성 완료!")

subjects = ["영어", "C언어", "파이썬"]
students = {}

while(1):
    drawStartMenu()
    n = int(input("번호 입력 : "))
    if n == 1:
        inputStudentData(students, subjects)
    elif n == 2:
        deleteStudentData()
    elif n == 3:
        searchStudentData()
    elif n == 4:
        showAllStudentGrade()
    elif n == 5:
        break

cursor.close()
db.close()
print("프로그램을 종료합니다.")