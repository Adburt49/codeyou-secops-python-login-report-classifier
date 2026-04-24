with open("logins.txt") as f:
    lines = f.readlines()

print(f"Loaded {len(lines)} login records.")

def new_func():
    successful_logins += 1
    return successful_logins

for line in lines:
    parts = line.strip().split()
    # parts = [username, ip, result]
    username, ip, result = parts

    is_int = ip.startswith("192.168.")
    location = "internal" if is_int else "external"
    status = "successful" if parts[2] == "Successful" else "failed"
    print(f"Login by {username} from {ip} ({location}) was {status}.")
    
    if status == "Failure":
        failed_logins += 1
    else:
        successful_logins = new_func() 
        
    if is_int:
         internal_logins += 1
    
    else:
         external_logins += 1    


print(f"\nSummary:")
print(f"Total logins: {len(lines)}")
print(f"Failed logins: {failed_logins}")  
print(f"Successful logins: {successful_logins}")
print(f"Internal logins: {internal_logins}")
print(f"External logins: {external_logins}")       