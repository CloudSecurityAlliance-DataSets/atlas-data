#!/usr/bin/env python3.12
"""
Analyze ATLAS.yaml structure for AICM control mapping strategy
"""

import yaml
from collections import defaultdict

def analyze_atlas_structure(atlas_file):
    """Analyze the ATLAS data structure and provide insights for control mapping"""
    
    with open(atlas_file, 'r') as f:
        data = yaml.safe_load(f)
    
    # Get the main matrix
    matrix = data['matrices'][0]
    tactics = matrix['tactics']
    techniques = matrix['techniques']
    
    print("=== ATLAS Structure Analysis ===\n")
    
    print(f"Total Tactics: {len(tactics)}")
    print(f"Total Techniques: {len(techniques)}")
    
    # Build tactic lookup
    tactic_lookup = {t['id']: t for t in tactics}
    
    # Count techniques per tactic
    tactic_technique_count = defaultdict(int)
    tactic_technique_list = defaultdict(list)
    
    for technique in techniques:
        if 'tactics' in technique:
            for tactic_id in technique['tactics']:
                tactic_technique_count[tactic_id] += 1
                tactic_technique_list[tactic_id].append({
                    'id': technique['id'],
                    'name': technique['name'],
                    'is_subtechnique': 'subtechnique-of' in technique
                })
    
    print("\n=== Tactics Overview ===")
    for tactic in tactics:
        tactic_id = tactic['id']
        tactic_name = tactic['name']
        count = tactic_technique_count[tactic_id]
        print(f"{tactic_id}: {tactic_name} ({count} techniques)")
    
    print("\n=== Detailed Breakdown by Tactic ===")
    for tactic in tactics:
        tactic_id = tactic['id']
        tactic_name = tactic['name']
        techniques_list = tactic_technique_list[tactic_id]
        
        print(f"\n{tactic_id}: {tactic_name}")
        print("-" * (len(tactic_id) + len(tactic_name) + 2))
        
        # Separate main techniques and subtechniques
        main_techniques = [t for t in techniques_list if not t['is_subtechnique']]
        subtechniques = [t for t in techniques_list if t['is_subtechnique']]
        
        print(f"Main Techniques ({len(main_techniques)}):")
        for tech in main_techniques:
            print(f"  • {tech['id']}: {tech['name']}")
        
        if subtechniques:
            print(f"Subtechniques ({len(subtechniques)}):")
            for tech in subtechniques:
                print(f"    ◦ {tech['id']}: {tech['name']}")
    
    return {
        'tactics': tactics,
        'techniques': techniques,
        'tactic_technique_mapping': dict(tactic_technique_list)
    }

if __name__ == "__main__":
    analyze_atlas_structure('../dist/ATLAS.yaml')
