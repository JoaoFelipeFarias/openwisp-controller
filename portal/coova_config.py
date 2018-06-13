with open('coova_config.default') as fh:
	count = 1
	for line in fh:
		if 'option defsessiontimeout' in line.strip():
			print(line)
			print(count)
		count += 1

print(count)