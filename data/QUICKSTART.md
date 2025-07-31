# AICM Control Mapping - Quick Start Guide

## Setup (First Time Only)

1. **Install Python dependencies:**
   ```bash
   pip install -r scripts/requirements.txt
   ```

2. **Generate the split data files:**
   ```bash
   python scripts/split_atlas_data.py --create-templates
   ```

## Generated Files

After running the setup, you'll have:

- **`tactics/`** - 15 ATLAS tactic files (YAML + JSON)
- **`mappings/`** - 15 empty control mapping templates
- **`examples/`** - Sample completed mapping

## Mapping Process

### 1. Choose a Tactic
Start with high-priority tactics (most techniques):
- `AML.TA0003-resource-development-controls.yaml` (12 techniques)
- `AML.TA0007-defense-evasion-controls.yaml` (8 techniques)
- `AML.TA0008-discovery-controls.yaml` (7 techniques)
- `AML.TA0011-impact-controls.yaml` (7 techniques)

### 2. Edit the Mapping File
Open a mapping file (e.g., `mappings/AML.TA0007-defense-evasion-controls.yaml`)

For each technique, fill in the AICM controls:
```yaml
aicm_controls:
  prevent: [AICM-XXX-001, AICM-YYY-002]  # Controls that prevent the technique
  detect: [AICM-MON-003]                  # Controls that detect the technique
  respond: [AICM-INC-001]                 # Controls that respond to the technique  
  recover: [AICM-BCR-001]                 # Controls that enable recovery
```

### 3. Add Mapping Notes
```yaml
mapping_notes: |
  Explanation of why these controls were selected,
  key considerations, and mapping rationale.
confidence_level: high  # low, medium, high
```

### 4. Update Metadata
```yaml
mapping_metadata:
  created_date: '2025-01-15'
  mapped_by: 'Your Name'
  review_status: completed  # pending, in-progress, completed
```

## Reference Files

- **`examples/completed-mapping-sample.yaml`** - Example of completed mapping
- **`tactics/tactics-summary.yaml`** - Overview of all tactics and technique counts
- **`README-AICM-MAPPING.md`** - Full project documentation

## Analysis

View ATLAS structure breakdown:
```bash
python scripts/analyze_atlas.py
```

## Tips

1. **Start with techniques you understand well** to build confidence
2. **Use the prevent/detect/respond/recover framework** systematically
3. **Reference the example mapping** for formatting and style
4. **Check technique descriptions** in the tactics files for context
5. **Work on one tactic at a time** for better focus