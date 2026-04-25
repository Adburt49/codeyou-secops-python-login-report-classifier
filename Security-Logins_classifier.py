from collections import defaultdict

# Ask user for filename
filename = input("Enter the log filename: ")

try:
    with open(filename) as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Error: {filename} not found.")
    exit()

print(f"Loaded {len(lines)} login records.")

total_attempts = 0
successful_logins = 0
failed_logins = 0
internal_ips = 0
external_ips = 0
failure_counts = defaultdict(lambda: defaultdict(int))  # user -> ip -> count

for line in lines:
    parts = line.strip().split()
    if len(parts) != 3:
        continue
    username, ip, result = parts
    print(f"User: {username}, IP: {ip}, Result: {result}")
    
    total_attempts += 1
    if result == "SUCCESS":
        successful_logins += 1
    else:
        failed_logins += 1
        failure_counts[username][ip] += 1
    
    # Classify IP (simple check for private ranges)
    ip_parts = ip.split('.')
    if len(ip_parts) == 4:
        first = int(ip_parts[0])
        second = int(ip_parts[1])
        if (first == 10) or (first == 172 and 16 <= second <= 31) or (first == 192 and second == 168):
            internal_ips += 1
        else:
            external_ips += 1

# Prepare summary output
summary = []
summary.append(f"Total login attempts: {total_attempts}")
summary.append(f"Successful logins: {successful_logins}")
summary.append(f"Failed logins: {failed_logins}")
summary.append(f"Internal IPs: {internal_ips}")
summary.append(f"External IPs: {external_ips}")
summary.append("\nPossible brute-force alerts:")

for user, ips in failure_counts.items():
    for ip, count in ips.items():
        if count >= 3:
            summary.append(f"User '{user}' had {count} failed logins from IP {ip}")

# Print to console
for line in summary:
    print(line)

# Write to summary.txt
with open("summary.txt", "w") as f:
    f.write("\n".join(summary))

print("\nSummary written to summary.txt")


