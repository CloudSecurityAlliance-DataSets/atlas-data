#!/usr/bin/env python3.12
"""
Split ATLAS.yaml data by tactics for AICM control mapping

This script extracts each tactic and its associated techniques into separate files
for easier AICM control mapping workflow.
"""

import yaml
import json
import os
from pathlib import Path
from collections import defaultdict
import argparse
import re
from datetime import date

def sanitize_filename(name):
    """Convert tactic name to filesystem-safe filename"""
    # Remove special characters and convert to lowercase with hyphens
    sanitized = re.sub(r'[^\w\s-]', '', name.lower())
    sanitized = re.sub(r'[-\s]+', '-', sanitized)
    return sanitized.strip('-')

def split_atlas_data(atlas_file, output_dir='data/tactics', output_format='both'):
    """
    Split ATLAS data by tactics into separate files
    
    Args:
        atlas_file: Path to ATLAS.yaml file
        output_dir: Directory to save split files
        output_format: 'yaml', 'json', or 'both'
    """
    
    # Load ATLAS data
    with open(atlas_file, 'r') as f:
        data = yaml.safe_load(f)
    
    # Get the main matrix
    matrix = data['matrices'][0]
    tactics = matrix['tactics']
    techniques = matrix['techniques']
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Build technique lookup by tactic
    tactic_techniques = defaultdict(list)
    
    for technique in techniques:
        if 'tactics' in technique:
            for tactic_id in technique['tactics']:
                tactic_techniques[tactic_id].append(technique)
    
    print(f"Splitting ATLAS data into {len(tactics)} tactic files...")
    
    # Process each tactic
    for tactic in tactics:
        tactic_id = tactic['id']
        tactic_name = tactic['name']
        tactic_techniques_list = tactic_techniques[tactic_id]
        
        # Create filename
        filename_base = f"{tactic_id}-{sanitize_filename(tactic_name)}"
        
        # Organize techniques by type (main techniques vs subtechniques)
        main_techniques = []
        subtechniques = []
        
        for tech in tactic_techniques_list:
            if 'subtechnique-of' in tech:
                subtechniques.append(tech)
            else:
                main_techniques.append(tech)
        
        # Create the data structure for this tactic
        tactic_data = {
            'tactic': {
                'id': tactic['id'],
                'name': tactic['name'],
                'description': tactic['description'],
                'object-type': tactic['object-type'],
                'created_date': tactic.get('created_date'),
                'modified_date': tactic.get('modified_date')
            },
            'summary': {
                'total_techniques': len(tactic_techniques_list),
                'main_techniques': len(main_techniques),
                'subtechniques': len(subtechniques)
            },
            'techniques': {
                'main_techniques': sorted(main_techniques, key=lambda x: x['id']),
                'subtechniques': sorted(subtechniques, key=lambda x: x['id'])
            }
        }
        
        # Add ATT&CK reference if present
        if 'ATT&CK-reference' in tactic:
            tactic_data['tactic']['ATT&CK-reference'] = tactic['ATT&CK-reference']
        
        # Save in requested format(s)
        if output_format in ['yaml', 'both']:
            yaml_file = os.path.join(output_dir, f"{filename_base}.yaml")
            with open(yaml_file, 'w') as f:
                yaml.dump(tactic_data, f, default_flow_style=False, sort_keys=False)
            print(f"  Created: {yaml_file}")
        
        if output_format in ['json', 'both']:
            json_file = os.path.join(output_dir, f"{filename_base}.json")
            with open(json_file, 'w') as f:
                json.dump(tactic_data, f, indent=2, ensure_ascii=False, default=str)
            print(f"  Created: {json_file}")
    
    # Create summary file
    summary_data = {
        'atlas_version': data.get('version', 'unknown'),
        'total_tactics': len(tactics),
        'total_techniques': len(techniques),
        'tactics_summary': []
    }
    
    for tactic in tactics:
        tactic_id = tactic['id']
        tech_count = len(tactic_techniques[tactic_id])
        summary_data['tactics_summary'].append({
            'id': tactic_id,
            'name': tactic['name'],
            'technique_count': tech_count,
            'filename': f"{tactic_id}-{sanitize_filename(tactic['name'])}"
        })
    
    # Save summary
    if output_format in ['yaml', 'both']:
        summary_file = os.path.join(output_dir, "tactics-summary.yaml")
        with open(summary_file, 'w') as f:
            yaml.dump(summary_data, f, default_flow_style=False, sort_keys=False)
        print(f"  Created summary: {summary_file}")
    
    if output_format in ['json', 'both']:
        summary_file = os.path.join(output_dir, "tactics-summary.json")
        with open(summary_file, 'w') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False, default=str)
        print(f"  Created summary: {summary_file}")
    
    print(f"\nSplit complete! {len(tactics)} tactic files created in {output_dir}/")
    
    return {
        'tactics_count': len(tactics),
        'techniques_count': len(techniques),
        'output_dir': output_dir,
        'files_created': len(tactics) * (2 if output_format == 'both' else 1) + (2 if output_format == 'both' else 1)
    }

def create_mapping_templates(tactics_dir='tactics', mappings_dir='mappings'):
    """
    Create template mapping files for AICM controls
    """
    
    Path(mappings_dir).mkdir(parents=True, exist_ok=True)
    
    # Find all tactic YAML files
    tactics_files = list(Path(tactics_dir).glob("AML.TA*.yaml"))
    
    print(f"Creating mapping templates for {len(tactics_files)} tactics...")
    
    for tactic_file in tactics_files:
        # Load tactic data
        with open(tactic_file, 'r') as f:
            tactic_data = yaml.safe_load(f)
        
        tactic_id = tactic_data['tactic']['id']
        tactic_name = tactic_data['tactic']['name']
        
        # Create mapping template
        mapping_template = {
            'tactic': {
                'id': tactic_id,
                'name': tactic_name,
                'description': tactic_data['tactic']['description'][:100] + "..." if len(tactic_data['tactic']['description']) > 100 else tactic_data['tactic']['description']
            },
            'mapping_metadata': {
                'created_date': None,
                'last_updated': None,
                'mapped_by': None,
                'review_status': 'pending'
            },
            'technique_mappings': []
        }
        
        # Add template for each technique
        all_techniques = tactic_data['techniques']['main_techniques'] + tactic_data['techniques']['subtechniques']
        
        for technique in all_techniques:
            technique_mapping = {
                'technique': {
                    'id': technique['id'],
                    'name': technique['name'],
                    'description': technique['description'][:150] + "..." if len(technique['description']) > 150 else technique['description'],
                    'is_subtechnique': 'subtechnique-of' in technique
                },
                'aicm_controls': {
                    'prevent': [],
                    'detect': [],
                    'respond': [],
                    'recover': []
                },
                'mapping_notes': "",
                'confidence_level': "low"  # low, medium, high
            }
            
            mapping_template['technique_mappings'].append(technique_mapping)
        
        # Save mapping template
        mapping_filename = tactic_file.stem + "-controls.yaml"
        mapping_file = Path(mappings_dir) / mapping_filename
        
        with open(mapping_file, 'w') as f:
            yaml.dump(mapping_template, f, default_flow_style=False, sort_keys=False)
        
        print(f"  Created: {mapping_file}")
    
    print(f"\nMapping templates created in {mappings_dir}/")

def main():
    parser = argparse.ArgumentParser(description="Split ATLAS data by tactics for AICM control mapping")
    parser.add_argument('--atlas-file', default='../dist/ATLAS.yaml', 
                       help='Path to ATLAS.yaml file (default: ../dist/ATLAS.yaml)')
    parser.add_argument('--output-dir', default='tactics',
                       help='Output directory for split files (default: tactics)')
    parser.add_argument('--format', choices=['yaml', 'json', 'both'], default='both',
                       help='Output format (default: both)')
    parser.add_argument('--create-templates', action='store_true',
                       help='Also create mapping template files')
    
    args = parser.parse_args()
    
    # Check if ATLAS file exists
    if not os.path.exists(args.atlas_file):
        print(f"Error: ATLAS file not found: {args.atlas_file}")
        return 1
    
    try:
        # Split the data
        result = split_atlas_data(args.atlas_file, args.output_dir, args.format)
        
        # Create mapping templates if requested
        if args.create_templates:
            create_mapping_templates(args.output_dir, 'mappings')
        
        print(f"\n✅ Success! Created {result['files_created']} files")
        print(f"   Tactics: {result['tactics_count']}")
        print(f"   Techniques: {result['techniques_count']}")
        print(f"   Output: {result['output_dir']}/")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
