numbers = (i for i in range(1, 101))

li_numbers = list(numbers)
nums=[]
samyukgu = ["3", "6", "9"]

for i in range(len(li_numbers)):
    nums.append(str(li_numbers[i]))

for a in range(len(nums)):
    if len(nums[a]) == 2:
        if nums[a][0] in samyukgu and nums[a][1] in samyukgu:
            li_numbers[a] = "짝짝"
        elif nums[a][0] in samyukgu or nums[a][1] in samyukgu:
            li_numbers[a] = "짝"
    elif len(nums[a]) == 1:
        if nums[a] in samyukgu:
            li_numbers[a] = "짝"

for j in range(len(li_numbers)):
    if j != 0 and j % 10 == 0:
        print("\n",li_numbers[j], end="")
    else:
        print(" ",li_numbers[j], end=" ")