#!/usr/bin/env python3
import os
import re

file_path = '/home/bdcrafte/myday.bdcrafter.com/dashboard/views.py'

print("=" * 50)
print("Fixing dashboard/views.py")
print("=" * 50)

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count how many fixes
    old_count = content.count('timezone.now().date()')
    
    # Replace all occurrences
    new_content = content.replace('timezone.now().date()', 'timezone.localtime(timezone.now()).date()')
    
    new_count = new_content.count('timezone.localtime(timezone.now()).date()')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Fixed {old_count} occurrence(s) of timezone.now().date()")
    print(f"✅ Now using timezone.localtime(timezone.now()).date()")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("=" * 50)
print("Done! Restart your app now.")