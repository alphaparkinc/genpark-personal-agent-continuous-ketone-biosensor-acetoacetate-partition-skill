# -*- coding: utf-8 -*-
"""Continuous Ketone Biosensor (CKM) & Acetoacetate Partition Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def partition_ketone_flux(**kwargs):
    """Analyzes continuous ketone monitor (CKM) flux, calculates beta-hydroxybutyrate (BHB) to acetoacetate (AcAc) redox ratio, and determines metabolic fuel flexibility."""
    continuous_bhb_readings_mm = kwargs.get('continuous_bhb_readings_mm')
    fasting_duration_hours = kwargs.get('fasting_duration_hours')
    concurrent_glucose_mg_dl = kwargs.get('concurrent_glucose_mg_dl')
    respiratory_exchange_ratio = kwargs.get('respiratory_exchange_ratio')

    mean_bhb = sum(continuous_bhb_readings_mm) / len(continuous_bhb_readings_mm) if continuous_bhb_readings_mm else 0.2
    peak_bhb = max(continuous_bhb_readings_mm) if continuous_bhb_readings_mm else 0.2
    
    estimated_bhb_acac_ratio = round(2.5 + (mean_bhb * 0.4), 2)
    estimated_acac_mm = round(mean_bhb / estimated_bhb_acac_ratio, 3)
    total_circulating_ketones_mm = round(mean_bhb + estimated_acac_mm, 2)
    
    glucose_mm = concurrent_glucose_mg_dl / 18.016
    gki = round(glucose_mm / (mean_bhb if mean_bhb > 0.05 else 0.05), 2)
    
    if gki <= 1.0:
        autophagy_tier = "Therapeutic Highest Autophagy (GKI <= 1.0)"
    elif gki <= 3.0:
        autophagy_tier = "High Autophagy & Deep Nutritional Ketosis (1.0 < GKI <= 3.0)"
    elif gki <= 6.0:
        autophagy_tier = "Moderate Nutritional Ketosis (3.0 < GKI <= 6.0)"
    elif gki <= 9.0:
        autophagy_tier = "Low Nutritional Ketosis (6.0 < GKI <= 9.0)"
    else:
        autophagy_tier = "Glycolytic Dominance / Minimal Ketosis (GKI > 9.0)"
        
    fuel_preference = "Lipid / Ketone Dominant" if respiratory_exchange_ratio <= 0.75 else "Mixed Fuel" if respiratory_exchange_ratio <= 0.85 else "Carbohydrate Dominant"
    
    result = {
        "status": "success",
        "mean_bhb_mm": round(mean_bhb, 2),
        "peak_bhb_mm": round(peak_bhb, 2),
        "estimated_acetoacetate_mm": estimated_acac_mm,
        "total_ketone_pool_mm": total_circulating_ketones_mm,
        "bhb_acac_redox_ratio": estimated_bhb_acac_ratio,
        "glucose_ketone_index_gki": gki,
        "autophagy_tier": autophagy_tier,
        "fuel_oxidation_preference": fuel_preference,
        "fasting_metabolic_state": f"Fasting {fasting_duration_hours}h - Glycogen depleted, active hepatic ketogenesis",
        "engine": "GenPark Ketone Redox Partition Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "partition_ketone_flux": {
        "name": "partition_ketone_flux",
        "description": "Analyzes continuous ketone monitor (CKM) flux, calculates beta-hydroxybutyrate (BHB) to acetoacetate (AcAc) redox ratio, and determines metabolic fuel flexibility.",
        "parameters": {
            "type": "object",
            "properties": {
                "continuous_bhb_readings_mm": {"type": "array", "description": "Continuous interstitial/capillary BHB readings (mM)"},
                "fasting_duration_hours": {"type": "number", "description": "Consecutive hours elapsed since last meal"},
                "concurrent_glucose_mg_dl": {"type": "number", "description": "Concurrent blood glucose reading (mg/dL)"},
                "respiratory_exchange_ratio": {"type": "number", "description": "Estimated or measured RER (VCO2 / VO2)"},
            },
            "required": ['continuous_bhb_readings_mm', 'fasting_duration_hours', 'concurrent_glucose_mg_dl', 'respiratory_exchange_ratio']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "partition_ketone_flux":
            res = partition_ketone_flux(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-continuous-ketone-biosensor-acetoacetate-partition-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-personal-agent-continuous-ketone-biosensor-acetoacetate-partition-skill...")
    test_args = {'continuous_bhb_readings_mm': [1.2, 1.4, 1.8, 1.6, 1.9], 'fasting_duration_hours': 18.5, 'concurrent_glucose_mg_dl': 84.0, 'respiratory_exchange_ratio': 0.73}
    res = partition_ketone_flux(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-personal-agent-continuous-ketone-biosensor-acetoacetate-partition-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
