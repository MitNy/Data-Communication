import struct

file = open("./studentinfo.txt", "rb")
data = file.read()

data_list = []
kim_list = {}
lee_list = {}
num_list = []
for i in range(1,46):
	num = data[(16*(i-1)):(16*(i-1))+1]
	#num = data[0:1]
	name = data[(16*(i-1))+1 : (16*(i-1))+10]
	#name = data[1:10]

	grade = data[(16*i)-5 : (16*i)-4]
	#grade = data[11:12]
	age = data[(16*i)-3 : (16*i)]
	#age = data[13:16]

	data_num = struct.unpack("!b",num)
	data_name = name.decode()
	data_grade = struct.unpack("!b",grade)
	data_age = struct.unpack("!3b",age)

	data_list.append([data_num[0],data_name,data_grade[0],data_age[2]])

	num_list.append(data_num[0])
	if data_name[0] == '김':
		kim_list[data_name] = data_age[2]	

	if data_name[0] == '이':
		lee_list[data_name] = data_age[2]


# All list output
for j in range(0,45):
	print(data_list[j])

print('\n')
# Kim average age output
age_list = list(kim_list.values())
average_age = 0
for a in range(0,len(age_list)):
	average_age += age_list[a]
print(kim_list)
print("a.김씨들의 평균 나이는",average_age/len(age_list),"입니다.")
print('\n')

# The oldest LEE output
age_list2 = list(lee_list.values())
oldest_age = 0
print(lee_list)
max_age = max(age_list2)
for age_list2, oldest_age in lee_list.items():
	if oldest_age == max_age:
		print("b.이씨들 중 나이가 제일 많은 사람은",age_list2,"이고 나이는",max_age,"입니다.")
print('\n')

# number of each student number
num_count = {}

for stuNum in num_list:
	try: num_count[stuNum] += 1
	except: num_count[stuNum] = 1

sorted_num = sorted(num_count.items())
print(sorted_num)
print("c.각 학번 별 인원 수")

for p in range(0,len(sorted_num)):
	print(sorted_num[p][0],"학번은",sorted_num[p][1],"명 입니다.")

file.close()

