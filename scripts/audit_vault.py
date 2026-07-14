import os
import re
import json

def analyze_vault(root_dir):
    stats = {
        "total_files": 0,
        "total_links": 0,
        "files_with_frontmatter": 0,
        "files_without_frontmatter": 0,
        "possible_orphans": 0,
        "dirs_distribution": {}
    }
    
    all_files = []
    link_pattern = re.compile(r'\[\[(.*?)\]\]')
    
    # Pass 1: Collect files
    for r, d, f in os.walk(root_dir):
        if '.git' in r or '.obsidian' in r or '.agents' in r or 'scripts' in r:
            continue
        
        md_files = [file for file in f if file.endswith('.md')]
        stats["total_files"] += len(md_files)
        
        rel_dir = os.path.relpath(r, root_dir)
        stats["dirs_distribution"][rel_dir] = len(md_files)
        
        for file in md_files:
            all_files.append(os.path.join(r, file))
            
    # Remove empty dirs from stats
    stats["dirs_distribution"] = {k: v for k, v in stats["dirs_distribution"].items() if v > 0}
    
    # We will just sample up to 1000 files to avoid taking forever if there are 24k files
    import random
    sample_files = random.sample(all_files, min(1000, len(all_files)))
    
    frontmatter_count = 0
    link_count = 0
    orphan_count = 0
    
    for filepath in sample_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check frontmatter
                if content.startswith('---'):
                    frontmatter_count += 1
                
                # Check links
                links = link_pattern.findall(content)
                link_count += len(links)
                
                if len(links) == 0:
                    orphan_count += 1
                    
        except Exception as e:
            pass
            
    if len(sample_files) > 0:
        multiplier = stats["total_files"] / len(sample_files)
        stats["estimated_frontmatter"] = int(frontmatter_count * multiplier)
        stats["estimated_links"] = int(link_count * multiplier)
        stats["estimated_orphans"] = int(orphan_count * multiplier)
        stats["cohesion_score_est"] = round(100 - ((orphan_count / len(sample_files)) * 100), 2)
    
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    analyze_vault(r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica")
