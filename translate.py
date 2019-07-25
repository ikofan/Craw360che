import openpyxl


wb = openpyxl.load_workbook("D:\\360che\\dict.xlsx")
ws = wb.active

cn = []
en = []
for cell in ws["A"]:
    cn.append(str(cell.value))

for cell in ws["B"]:
    en.append(str(cell.value))

# zh_hans = tuple(cn)
# dict_list = dict.fromkeys(zh_hans)

dict_list = dict(zip(cn, en))
# 一开始还不会把列表转为字典，上面这个方法简单啊，学习了。

print(dict_list)
