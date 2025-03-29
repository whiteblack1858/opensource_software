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


# 학생 등수 계산
def rankStudent(students):
    total_scores = [student.total for student in students.values()] #모든 학생들의 평균 점수를 배열로 저장
    sorted_scores = sorted(total_scores, reverse=True) # 저장한 배열을 내림차순으로 정렬
    for student in students.values():
        student.rank = sorted_scores.index(student.total) + 1 


#학생 객체 생성 및 이름과 학번 입력 함수
def inputStudentData(students, subjects):
    if len(students) >= 5:
        print("더 이상 입력할 수 없습니다.")
    else:
        name = input("학생 이름 입력: ")
        number = int(input("학생 학번 입력: "))
        students[name] = Student(name, number)
        students[name].input_scores(subjects)
        rankStudent(students)
        print("입력 완료!")


#학생 삭제 함수    
def deleteStudentData(students):
    name = input("삭제할 학생 이름 입력: ")
    stdNumber = int(input("학생 학번 입력: "))
    if students[name].number == stdNumber:
        print(f"{name} 학생을 삭제합니다.\n")
        del students[name]
        rankStudent(students)
    else:
        print(f"학생 이름 또는 학생 이름이 잘못되었습니다.\n")


#학생 탐색 함수
def searchStudentData(students):
    name = input("검색할 학생 이름 입력: ")
    stdNumber = int(input("검색할 학생 학번 입력: "))
    if students[name].number == stdNumber:
        print(f"{stdNumber}의 {name} 학생이 존재합니다.\n")
        s = students[name]
        drawMiniMenu()
        print(f"{s.name}    {s.scores['영어']}    {s.scores['C언어']}    {s.scores['파이썬']}\    "
            f"{s.total}    {s.average:.2f}    {s.grade}    {s.rank}")
    else:
        print(f"학생 이름 또는 학생 이름이 잘못되었습니다.\n")


#80점 이상 학생 수 카운트 함수
def highGradeStudentCount(students):
    cnt = 0
    for student in students.values():
        if student.average >= 80.0:
            cnt += 1
    return cnt

#전체 학생 성적 조회
def showAllStudentGrade(students):
    n = highGradeStudentCount(students)

    c = input("총점 기준으로 학생들을 정렬하시겠습니까?(Y/N) : ")
    if c=='Y':
        sorted_students = sorted(students.values(), key=lambda student: student.total, reverse=True)
        drawMiniMenu()
        for student in sorted_students:
            print(f"{student.name}\t{student.scores['영어']}\t\t{student.scores['C언어']}\t\t{student.scores['파이썬']}\t\t"
                f"{student.total}\t\t{student.average:.2f}\t\t{student.grade}\t\t{student.rank}")
        print(f"80점 이상인 학생 수 : {n}")

    else:
        drawMiniMenu()
        for student in students.values():
            print(f"{student.name}\t{student.scores['영어']}\t\t{student.scores['C언어']}\t\t{student.scores['파이썬']}\t\t"
                f"{student.total}\t\t{student.average:.2f}\t\t{student.grade}\t\t{student.rank}")
        print(f"80점 이상인 학생 수 : {n}")


num_students = 5
subjects = ["영어", "C언어", "파이썬"]
students = {}

while(1):
    drawStartMenu()
    n = int(input("번호 입력 : "))
    if n == 1:
        inputStudentData(students, subjects)
    elif n == 2:
        deleteStudentData(students)
    elif n == 3:
        searchStudentData(students)
    elif n ==4:
        showAllStudentGrade(students)
    elif n ==5:
        break




