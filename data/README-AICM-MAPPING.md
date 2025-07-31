# AICM 1.0 to ATLAS TTPs Control Mapping Project

This project maps AICM 1.0 security controls (200+ AI-related security controls) to individual ATLAS (Adversarial Threat Landscape for AI Systems) Tactics, Techniques, and Procedures (TTPs).

## Project Overview

**Goal**: For each ATLAS TTP, identify which AICM controls would:
- **Prevent** the technique from occurring
- **Detect** when the technique is being attempted  
- **Respond** to/mitigate the technique's impact
- **Recover** from successful technique execution

## ATLAS Structure Summary

- **15 Tactics** - High-level adversary goals (like a kill chain)
- **115 Main Techniques** - Specific methods to achieve tactical goals
- **105+ Subtechniques** - Variations of main techniques
- **Total TTPs**: 220+ individual items to map

## Tactics Breakdown by Volume

### High-Priority Tactics (Most Techniques)
- **AML.TA0003: Resource Development** (12 techniques) - Supply chain, training data poisoning
- **AML.TA0007: Defense Evasion** (8 techniques) - Jailbreaking, evasion, manipulation
- **AML.TA0008: Discovery** (7 techniques) - Model probing, information gathering  
- **AML.TA0011: Impact** (7 techniques) - Model integrity, service denial, external harms

### Medium-Priority Tactics
- **AML.TA0002: Reconnaissance** (6 techniques) - Intelligence gathering
- **AML.TA0004: Initial Access** (6 techniques) - Entry points into AI systems
- **AML.TA0010: Exfiltration** (5 techniques) - Data/model extraction

### Lower-Volume Tactics
- **AML.TA0000: AI Model Access** (4 techniques) - API access, physical access
- **AML.TA0005: Execution** (4 techniques) - Prompt injection, code execution
- **AML.TA0006: Persistence** (4 techniques) - Maintaining access
- **AML.TA0001: AI Attack Staging** (4 techniques) - Attack preparation
- **AML.TA0009: Collection** (3 techniques) - Data gathering
- **AML.TA0012: Privilege Escalation** (2 techniques) - Permission escalation
- **AML.TA0013: Credential Access** (1 technique) - Credential theft
- **AML.TA0014: Command and Control** (1 technique) - Remote control

## Directory Structure

```
├── README-AICM-MAPPING.md          # This file
├── scripts/
│   ├── split_atlas_data.py         # Split ATLAS.yaml by tactics
│   ├── analyze_atlas.py            # Analyze ATLAS structure
│   └── requirements.txt            # Python dependencies
├── tactics/                        # Split data by tactic (YAML/JSON)
│   ├── AML.TA0002-reconnaissance.yaml
│   ├── AML.TA0003-resource-development.yaml  
│   ├── tactics-summary.yaml        # Overview of all tactics
│   └── ...
├── mappings/                       # AICM control mappings
│   ├── AML.TA0002-controls.yaml
│   ├── example-mapping.yaml        # Example completed mapping
│   └── ...
└── examples/
    └── completed-mapping-sample.yaml  # Sample of completed control mapping
```

## Usage

### 1. Split ATLAS Data by Tactics
```bash
python scripts/split_atlas_data.py --atlas-file ../dist/ATLAS.yaml
```

This creates individual files for each tactic containing:
- Tactic metadata (ID, name, description)
- All techniques belonging to that tactic
- Both YAML and JSON formats for flexibility

### 2. Analyze ATLAS Structure
```bash
python scripts/analyze_atlas.py
```

Provides overview of tactics, techniques, and their relationships.

### 3. Create Control Mappings
For each tactic file in `data/tactics/`, create corresponding control mapping files in `data/mappings/`.

## Mapping Methodology

### For Each Technique:
1. **Analyze the technique description** and understand the attack method
2. **Identify applicable AICM controls** that address the technique
3. **Categorize control relationships**:
   - `prevent`: Controls that stop the technique from occurring
   - `detect`: Controls that identify when technique is attempted
   - `respond`: Controls that mitigate technique impact
   - `recover`: Controls that restore normal operations

### Example Mapping Structure:
```yaml
technique_id: AML.T0020
technique_name: Poison Training Data
aicm_controls:
  prevent:
    - AICM-GOV-001  # Data governance
    - AICM-DAT-003  # Data validation
  detect:
    - AICM-MON-005  # Training monitoring
    - AICM-AUD-002  # Data auditing
  respond:
    - AICM-INC-001  # Incident response
  recover:
    - AICM-BCR-004  # Model recovery
```

## Tools and Scripts

### split_atlas_data.py
Main data processing script that:
- Splits ATLAS.yaml into 15 separate tactic files
- Creates both YAML and JSON formats
- Generates mapping templates with proper structure
- Includes comprehensive metadata tracking

**Options:**
```bash
python scripts/split_atlas_data.py --help
  --atlas-file PATH        Path to ATLAS.yaml (default: ../dist/ATLAS.yaml)
  --output-dir DIR         Output directory (default: tactics)
  --format {yaml,json,both} Output format (default: both)
  --create-templates       Also create mapping template files
```

### analyze_atlas.py  
Analysis tool that provides:
- Complete breakdown of all 15 tactics
- Technique counts per tactic
- Detailed listing of main techniques vs subtechniques
- Strategic insights for prioritizing mapping work

### requirements.txt
Python dependencies: `PyYAML==6.0.1`

## File Formats and Structure

### Tactic Files (`tactics/`)
Each tactic file contains:
```yaml
tactic:                    # Basic tactic information
  id: AML.TA0007          # ATLAS tactic ID
  name: Defense Evasion   # Human-readable name
  description: "..."      # Full description
  created_date: "..."     # When tactic was created
  modified_date: "..."    # Last modification

summary:                  # Quick statistics
  total_techniques: 8     # Total techniques for this tactic
  main_techniques: 8      # Main techniques (not subtechniques)
  subtechniques: 0        # Subtechnique count

techniques:               # All techniques under this tactic
  main_techniques: [...]  # Array of main technique objects
  subtechniques: [...]    # Array of subtechnique objects
```

### Mapping Files (`mappings/`)
Template structure for control assignments:
```yaml
tactic: {...}            # Tactic metadata (reference only)

mapping_metadata:        # Tracking information
  created_date: null     # When mapping was created
  mapped_by: null        # Who created the mapping
  review_status: pending # pending/in-progress/completed

technique_mappings:      # Array of technique mappings
- technique: {...}       # Technique metadata
  aicm_controls:         # Control assignments
    prevent: []          # Controls that prevent technique
    detect: []           # Controls that detect technique  
    respond: []          # Controls that respond to technique
    recover: []          # Controls that enable recovery
  mapping_notes: ""      # Rationale and considerations
  confidence_level: low  # low/medium/high
```

### Summary Files
- `tactics-summary.yaml` - Overview of all tactics with technique counts
- `examples/completed-mapping-sample.yaml` - Fully worked example

## Next Steps

1. **Start with high-priority tactics** (Resource Development, Defense Evasion, Impact)
2. **Use the mapping templates** in `mappings/` directory for systematic control assignment
3. **Reference the example** in `examples/completed-mapping-sample.yaml`
4. **Build comprehensive matrix** showing Control-to-Technique relationships
5. **Validate mappings** with security experts
6. **Generate reports** showing coverage and gaps

## Moving This Package

This entire `data/` directory is self-contained and portable:
- All scripts use relative paths
- All dependencies are documented
- Complete documentation included
- Ready-to-use templates provided

Simply move the entire directory and run `pip install -r scripts/requirements.txt` to get started.