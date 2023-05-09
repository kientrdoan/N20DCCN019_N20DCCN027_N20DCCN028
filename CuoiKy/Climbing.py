"""
    Trương Thái Hoàng - N20DCCN019
    Đoàn Trung Kiên - N20DCCN027
    Lê Ngọc Tuấn Kiệt - N20DCCN028
"""

from copy import deepcopy
import time
start_time = time.time()

def read_file(path):
    class_available = []
    with open(path, "r") as f:
        data = f.readlines()
        for i in range(0, len(data)):
            data[i] = data[i].split(" ")
            data[i] = [x.strip() for x in data[i]]
            data[i] = list(filter(bool, data[i]))
            class_available.append(data[i])
    return class_available

#Kiem tra lop co the hoc vao tiet bat buoc
def checkMandatory(mandatory_day, class_available):
    for i in range(1, len(mandatory_day)):
        for j in range(1, len(mandatory_day[i])):
            if (int(mandatory_day[i][j])==1) and (int(class_available[i][j]) != 1):
                return False, mandatory_day[i][0], mandatory_day[0][j - 1]
    return True, None, None

#teacher, class, period la index
def gradeCal(teacher_class, mandatory_day, schedule, teacher_available, class_available, period, Class, teacher, currentTeacher, countMan):
    
    grade=0
    #Tong So Tiet Giao Vien Day Cho Tung Lop
    if int(teacher_class[teacher][Class]) <1 :
        grade -= 10000
    else:
        grade+=(int(teacher_class[teacher][Class]))*100

    #Tiet khong bat buoc phai hoc
    if mandatory_day[period][Class]=="0" and countMan>0:
        grade-=10000

    #Tiet Ma Lop Khong The Hoc
    if class_available[period][Class]=="0":
        grade-=10000
    
    #GV Khong The Day 
    if teacher_available[period][teacher]=="0":
        grade-=10000
    
    #Giao Vien Day Hai Lop Cung Tiet
    try:
        schedule[period].index(teacher)
        grade-=10000
    except:
        None

    #So giáo viên có thể dạy cho lớp
    countAvailableTeachers=0
    for i in range(1, len(teacher_class)):
        if int(teacher_class[i][Class])>0:
            countAvailableTeachers+=1
            #Neu Ma GV Da Co Tiet
            try:
                schedule[period].index(i)
                countAvailableTeachers-=1
            except:
                None 

    if currentTeacher != "X":
        grade-=7000
    
    #Uu tien giao vien con nhieu tiet hon
    for i in range(1, len(teacher_class[1])):
        grade+=int(teacher_class[teacher][i])

    grade+=(len(teacher_available[0])-countAvailableTeachers-1)*1000
    return grade

def convert(schedule, teachers):
    for i in range(1, len(schedule)):
        for j in range(1, len(schedule[i])):
            if schedule[i][j]=="X": 
                continue
            schedule[i][j] = teachers[schedule[i][j]-1]
    return schedule

def addTeacher(schedule, class_available, teacher_available, teacher_class, mandatory_day, periodNum, countMan, grade):
    biggestGrade = grade
    biggestTeacher=0 #Index
    biggestClass=0 #Index
    biggestPeriod=0 #Index

    for period in range(1, len(schedule)): #Duyet qua tat ca cac tiet
        for Class in range(1, len(schedule[period])): #Duyet qua tat ca cac lop
            for teacher in range(1, len(teacher_available[1])): #Duyet qua tung giao vien
                if teacher == schedule[period][Class]: 
                    continue
                currentTeacher = schedule[period][Class] #Lay GV
                currentGrade = grade + gradeCal(teacher_class, mandatory_day, schedule, teacher_available, class_available, period, Class, teacher, currentTeacher, countMan)
                if currentGrade>biggestGrade:
                    biggestGrade = currentGrade
                    #Lay Vi Tri
                    biggestClass = Class
                    biggestPeriod = period
                    biggestTeacher = teacher
    if biggestTeacher == 0:
        for i in range(1, len(teacher_class)):
            for j in range(1, len(teacher_class[i])):
                if int(teacher_class[i][j]) != 0:
                    #print("Lịch xếp chưa hoàn thành:")
                    schedule=convert(schedule, teacher_available[0])
                    for i in range(len(schedule)):
                        print(schedule[i])
                    file = open("out_put.csv", "w", encoding= "utf-8")
                    out_put(schedule, file)
                    #print("Các tiết bị dư ra là:")
                    for i in range(len(teacher_class)):
                        print(teacher_class[i])
                    file.write("\n\nCac, tiet, bi, du, ra, la:\n")
                    out_put(teacher_class, file)
                    exit()
        print("Xep lich xong!")
        convert(schedule, teacher_available[0])
        for i in range(len(schedule)):
            print(schedule[i])
        file = open("out_put.csv", "w", encoding= "utf-8")
        out_put(schedule, file)
        exit()
        
    else:
        if schedule[biggestPeriod][biggestClass] == "X":
            periodNum-=1
        else:
            teacher_class[schedule[biggestPeriod][biggestClass]][biggestClass] = int(teacher_class[biggestTeacher][biggestClass])+1
        if mandatory_day[biggestPeriod][biggestClass] == "1":
            countMan-=1
        #So tiet giao vien day cho mot lop
        teacher_class[biggestTeacher][biggestClass]= int(teacher_class[biggestTeacher][biggestClass])-1
        #The Vi Tri Cua GV
        schedule[biggestPeriod][biggestClass] = biggestTeacher
    return schedule, teacher_class, periodNum, countMan, biggestGrade


def climbing(schedule, class_available, teacher_available, teacher_class, mandatory_day):
    #Tong so tiet giao vien day
    periodNum=0
    for i in range(1, len(teacher_class)):
        for j in range(1, len(teacher_class[i])):
            periodNum += int(teacher_class[i][j])
    
    countMan = 0 #So tiet bat buoc
    countAvail=0 #So tiet lop co the hoc
    for i in range(1, len(class_available)):
        for j in range(1, len(class_available[1])):
            if class_available[i][j]=="1":
                countAvail+=1
            if mandatory_day[i][j]=="1":
                countMan+=1
    if countAvail < periodNum:
        print("Số tiết cần dạy nhiều hơn số tiết các lớp có thể học")
        exit()
    grade=0
    for i in range(1, len(teacher_class)):
        for j in range(1, len(teacher_class[i])):
            grade-= int(teacher_class[i][j])*1000
    
    while True:
        print("So tiet chua xep: ",periodNum)
        schedule, teacher_class, periodNum, countMan, grade = addTeacher(schedule, class_available, teacher_available, teacher_class, mandatory_day, periodNum, countMan, grade)
    # return schedule, teacher_class

def out_put(schedule, file):
    # print(schedule)
    # file = open("out_put.csv", "w", encoding= "utf-8")
    first_line = ","
    for i in range(len(schedule[0])):
        first_line += schedule[0][i] + ","
    file.write(first_line+"\n")

    for i in range(1, len(schedule)):
        line = ""
        for j in range(len(schedule[i])):
            line += str(schedule[i][j]) + ","
        
        line += "\n"
        file.write(line)

if __name__ == "__main__":
    class_available = read_file("Class-Available.txt")
    mandatory_day = read_file("Mandatory-Days.txt")
    teacher_available = read_file("Teacher-Available.txt")
    teacher_class = read_file("Teacher-Class.txt")
    canSchedule=True
    canSchedule, cannotPeriod, cannotClass = checkMandatory(mandatory_day, class_available)
    if(not canSchedule):
        print("Lớp "+ str(cannotClass) + " không thể học vào tiết "+str(cannotPeriod)+" theo lịch học bắt buộc")
    else:
        #Khoi tao schedule
        schedule=[class_available[0]]
        for i in range(48):
            date=[]
            period="T"+str(int(i/8)+2)+"t"+str(int(i%8)+1)
            date+=[period]
            for j in range(len(teacher_class[0])):
                date+=["X"]
            schedule+=[date]
        
        #Bat dau xep thoi khoa bieu
        schedule, teacher_class = climbing(schedule, class_available, teacher_available, teacher_class, mandatory_day)