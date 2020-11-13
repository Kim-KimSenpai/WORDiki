import sqlite3

user_name = 'Robot1'
file_with_today_links = open('today_links_file.txt', 'w')
file_with_history = open('history.txt', 'r')
last_history = {}

length_of_history = int(file_with_history.readline().strip())
for i in range(length_of_history):
    s = file_with_history.readline().split()
    last_history[s[0]] = int(s[1])
file_with_history.close()

con = sqlite3.connect('C:\\Users\\' + user_name + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History')
cursor = con.cursor()
cursor.execute("SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;")
results = cursor.fetchall()

file_with_history = open('history.txt', 'w')
file_with_history.write(str(len(results)) + '\n')

for (link, counter) in results:
    if link in last_history and last_history[link] != counter or link not in last_history:
        file_with_today_links.write(link + '\n')
    file_with_history.write(link + ' ' + str(counter) + '\n')

file_with_today_links.close()
file_with_history.close()