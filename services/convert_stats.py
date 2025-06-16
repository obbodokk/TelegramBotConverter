import os
import csv
from datetime import datetime
from config import DATA_DIR, STATS_FILE


def stats_file():
    if not os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'source_format', 'target_format', 'count'])

def log_of_convertation(source_format, target_format):
    stats_file()
    
    stats = []
    with open(STATS_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        stats = list(reader)

    found = False
    for row in stats:
        if row['source_format'] == source_format and row['target_format'] == target_format:
            row['count'] = str(int(row['count']) + 1)
            found = True
            break

    if not found:
        stats.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_format': source_format,
            'target_format': target_format,
            'count': '1'
        })
    
    with open(STATS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'source_format', 'target_format', 'count'])
        writer.writeheader()
        writer.writerows(stats)

def get_top_conversions(limit=10):
    stats_file()
    
    with open(STATS_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        stats = list(reader)
    

    sorted_stats = sorted(stats, key=lambda x: int(x['count']), reverse=True)
    
    return sorted_stats[:limit]