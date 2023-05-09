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

def checkMandatory(mandatory_day, class_available):
    for i in range(1, len(mandatory_day)):
        for j in range(1, len(mandatory_day[i])):
            if (int(mandatory_day[i][j])==1) and (int(class_available[i][j]) != 1):
                return False, mandatory_day[i][0], mandatory_day[0][j - 1]
    return True, None, None

def gradeCal(teacher_class, mandatory_day, schedule, teacher_available, class_available, period, Class, teacher, currentTeacher, countMan):
    grade=0
    says=""
    if int(teacher_class[teacher][Class])<1:
        grade-=1000
    else:
        grade+=int(teacher_class[teacher][Class])
    if mandatory_day[period][Class]=="0" and countMan>0:
        grade-=1000
    if class_available[period][Class]=="0":
        grade-=1000
    if teacher_available[period][teacher]=="0":
        grade-=1000
    try:
        schedule[period].index(teacher)
        grade-=1000
    except:
        None
    countAvailableTeachers=0
    for i in range(1, len(teacher_class)):
        if int(teacher_class[i][Class])>0:
            countAvailableTeachers+=1
            try:
                schedule[period].index(i)
                countAvailableTeachers-=1
            except:
                None 
    if currentTeacher!="X":
        grade-=100
    grade+=len(teacher_available[0])-countAvailableTeachers-1
    return grade

def convert(schedule, teachers):
    for i in range(1, len(schedule)):
        for j in range(1, len(schedule[i])):
            if schedule[i][j]=="X": continue
            schedule[i][j]=teachers[schedule[i][j]-1]
    return schedule

def addTeacher(schedule, class_available, teacher_available, teacher_class, mandatory_day, periodNum, countMan):
    biggestGrade = -10000
    biggestTeacher=0
    biggestClass=0
    biggestPeriod=0
    for period in range(1, len(mandatory_day)):
        for Class in range(1, len(mandatory_day[period])):
            for teacher in range(1, len(teacher_available[1])):
                if teacher==schedule[period][Class]: continue
                currentTeacher=schedule[period][Class]
                currentGrade = gradeCal(teacher_class, mandatory_day, schedule, teacher_available, class_available, period, Class, teacher, currentTeacher, countMan)
                if currentGrade>biggestGrade:
                    biggestGrade=currentGrade
                    biggestClass=Class
                    biggestPeriod=period
                    biggestTeacher=teacher
    if biggestTeacher==0:
        print("Lịch xếp chưa hoàn thành:")
        schedule=convert(schedule, teacher_available[0])
        for i in range(len(schedule)):
            print(schedule[i])
        file = open("out_put.csv", "w", encoding= "utf-8")
        out_put(schedule, file)
        print("Các tiết bị dư ra là:")
        for i in range(len(teacher_class)):
            print(teacher_class[i])
        file.write("\n\nCac, tiet, bi, du, ra, la:\n")
        out_put(teacher_class, file)
        exit()
    else:
        if schedule[biggestPeriod][biggestClass]=="X":
            periodNum-=1
        else:
            teacher_class[biggestClass][schedule[biggestPeriod][biggestClass]] = int(teacher_class[biggestClass][biggestTeacher])+1
        if mandatory_day[biggestPeriod][biggestClass]=="1":
            countMan-=1
        if biggestGrade<0:
            print("Here")
        teacher_class[biggestClass][biggestTeacher]= int(teacher_class[biggestClass][biggestTeacher])-1
        schedule[biggestPeriod][biggestClass]=biggestTeacher
    # if periodNum==252:
    #     print(schedule[biggestPeriod][biggestClass], biggestTeacher, biggestGrade, biggestClass, biggestPeriod)
    #     print()
    return schedule, teacher_class, periodNum, countMan


def climbing(schedule, class_available, teacher_available, teacher_class, mandatory_day):
    periodNum=0
    for i in range(1, len(teacher_class)):
        for j in range(1, len(teacher_class[i])):
            periodNum += int(teacher_class[i][j])
    countMan = 0
    countAvail=0
    for i in range(1, len(class_available)):
        for j in range(1, len(class_available[1])):
            if class_available[i][j]=="1":
                countAvail+=1
            if mandatory_day[i][j]=="1":
                countMan+=1
    if countAvail < periodNum:
        print("Số tiết cần dạy nhiều hơn số tiết các lớp có thể học")
        exit()
    print(countMan)
    while periodNum > 0:
        print("So tiet chua xep: ",periodNum)
        schedule, teacher_class, periodNum, countMan = addTeacher(schedule, class_available, teacher_available, teacher_class, mandatory_day, periodNum, countMan)
    return schedule, teacher_class

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
            line += schedule[i][j] + ","
        
        line += "\n"
        file.write(line)

if __name__ == "__main__":
    class_available = read_file("Class-Available.txt")
    mandatory_day = read_file("Mandatory-Days.txt")
    teacher_available = read_file("Teacher-Available.txt")
    teacher_class = read_file("Teacher-Class.txt")
    canSchedule=True
    canSchedule, cannotPeriod, cannotClass=checkMandatory(mandatory_day, class_available)
    if(not canSchedule):
        print("Lớp "+ str(cannotClass) + " không thể học vào tiết "+str(cannotPeriod)+" theo lịch học bắt buộc")
    else:
        schedule=[class_available[0]]
        for i in range(48):
            date=[]
            period="T"+str(int(i/8)+2)+"t"+str(int(i%8)+1)
            date+=[period]
            for j in range(len(teacher_class[0])):
                date+=["X"]
            schedule+=[date]
        schedule, teacher_class = climbing(schedule, class_available, teacher_available, teacher_class, mandatory_day)
        print("Xep lich xong!")
        convert(schedule, teacher_available[0])
        for i in range(len(schedule)):
            print(schedule[i])
        # print("Process finished --- %s seconds ---" % (time.time() - start_time))
        file = open("out_put.csv", "w", encoding= "utf-8")
        out_put(schedule, file)