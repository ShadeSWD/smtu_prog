#!/usr/bin/env python3
import cgi

form = cgi.FieldStorage()
name = form.getfirst("name", "empty")
group = form.getfirst("group", "empty")
print("Content-type: text/html\n")
print("""
<!DOCTYPE HTML>
<html>
<head>
	<meta charset="windows-1251">
	<title>Form processing</title>
</head>
<body>
""")
print("<h1>Processed form</h1>")
print(f"<p>Name: {name}</p>")
print(f"<p>Group: {group}</p>")
print("""
</body>
</html>
""")
