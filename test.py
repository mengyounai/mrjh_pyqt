# 执行命令
import re
import subprocess

command = 'where python'
process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, _ = process.communicate()

# 解码输出结果
output = output.decode('gbk')
# 去除换行符
output = output.strip()

# 使用正则表达式匹配路径中的 python.exe
pattern = r".*\\Python\\([^\\]+\\python\.exe)"
match = re.search(pattern, output)

if match:
    python_exe = match.group(1)
    full_path = match.group(0)
    print("Python文件夹路径:", full_path)
else:
    print("未找到符合条件的 python.exe")