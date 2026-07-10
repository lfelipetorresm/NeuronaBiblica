s1 = "ãñáöÞ"
s2 = "èåüðíåõóôïò"

print(s1.encode('windows-1252').decode('windows-1253'))
print(s2.encode('windows-1252').decode('windows-1253'))
