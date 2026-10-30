# Continuous Ketone Biosensor (CKM) & Acetoacetate Partition Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `partition_ketone_flux`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Analyzes continuous ketone monitor (CKM) flux, calculates beta-hydroxybutyrate (BHB) to acetoacetate (AcAc) redox ratio, and determines metabolic fuel flexibility.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Personal Agent (Bio / Ketogenic Metabolism)`

## MCP Tool Specification
### `partition_ketone_flux`
Parameters:
- `continuous_bhb_readings_mm` (list): Continuous interstitial/capillary BHB readings (mM)
- `fasting_duration_hours` (float): Consecutive hours elapsed since last meal
- `concurrent_glucose_mg_dl` (float): Concurrent blood glucose reading (mg/dL)
- `respiratory_exchange_ratio` (float): Estimated or measured RER (VCO2 / VO2)

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-personal-agent-continuous-ketone-biosensor-acetoacetate-partition-skill": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-continuous-ketone-biosensor-acetoacetate-partition-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
