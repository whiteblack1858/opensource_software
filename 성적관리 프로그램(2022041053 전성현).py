class Student:
    def __init__(self, name):
        self.name = name
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



num_students = 5
subjects = ["영어", "C언어", "파이썬"]
students = {}

# 학생 객체 생성
for i in range(num_students):
    name = input("학생이름 입력: ")
    students[name] = Student(name)

# 학생 점수 입력
for student in students.values(): #딕셔너리의 값을 호출해야 함
    student.input_scores(subjects)

# 학생 등수 계산
total_scores = [student.total for student in students.values()] #모든 학생들의 평균 점수를 배열로 저장
sorted_scores = sorted(total_scores, reverse=True) # 저장한 배열을 내림차순으로 정렬

for student in students.values():
    student.rank = sorted_scores.index(student.total) + 1 

print("\n학생 성적 결과\n")
print('-'*60)
print("이름\t영어\tC언어\t파이썬\t총점\t평균\t학점\t등수")
print('-'*60)

for student in students.values():
    print(f"{student.name}\t{student.scores['영어']}\t\t{student.scores['C언어']}\t\t{student.scores['파이썬']}\t\t"
          f"{student.total}\t\t{student.average:.2f}\t\t{student.grade}\t\t{student.rank}")