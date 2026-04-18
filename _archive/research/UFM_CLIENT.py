#!/usr/bin/env python3
"""
UFM Engine Client
Wrapper for Universal Format Message Engine API
Integrates the 7-stage universal pipeline for entity analysis
"""

import urllib.request
import json
import base64
from typing import Dict, Any, Optional

class UFMClient:
    """Client for UFM Engine API with universal endpoint support"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://ufm-engine.onrender.com"
        self.headers = {
            "Content-Type": "application/json",
            "X-Api-Key": api_key
        }
    
    def _request(self, endpoint: str, method: str = "POST", data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to UFM Engine"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "POST" and data:
                body = json.dumps(data).encode('utf-8')
                req = urllib.request.Request(url, data=body, headers=self.headers, method=method)
            else:
                req = urllib.request.Request(url, headers=self.headers, method=method)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result
        
        except urllib.error.HTTPError as e:
            return {
                "error": str(e),
                "status_code": e.code,
                "reason": e.reason
            }
        except Exception as e:
            return {
                "error": str(e),
                "status_code": 500
            }
    
    def health(self) -> Dict[str, Any]:
        """Check API health (no auth required)"""
        url = f"{self.base_url}/v1/health"
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def process_universal(self, data: bytes, verify: bool = True) -> Dict[str, Any]:
        """
        Run UFM's 7-stage universal pipeline.
        
        Returns structural analysis with:
        - quality_score (0.0-1.0)
        - 7 causal principles per stage
        - seed (deterministic)
        - replay validation
        - stage completion info
        """
        data_b64 = base64.b64encode(data).decode('utf-8')
        
        payload = {
            "data_b64": data_b64,
            "verify": verify
        }
        
        result = self._request("/v1/process/universal", "POST", payload)
        return result
    
    def process(self, data: bytes, symbol_length_mode: str = "auto_curve") -> Dict[str, Any]:
        """
        Standard process endpoint (fallback).
        Returns primitives, signature, discovery rate.
        """
        data_b64 = base64.b64encode(data).decode('utf-8')
        
        payload = {
            "data_b64": data_b64,
            "symbol_length_mode": symbol_length_mode
        }
        
        result = self._request("/v1/process", "POST", payload)
        return result
    
    def reconstruct(self, data: bytes) -> Dict[str, Any]:
        """Verify round-trip integrity (lossless)"""
        data_b64 = base64.b64encode(data).decode('utf-8')
        
        payload = {"data_b64": data_b64}
        result = self._request("/v1/reconstruct", "POST", payload)
        return result
    
    def replay(self, seed: int) -> Dict[str, Any]:
        """Replay data by seed"""
        result = self._request(f"/v1/replay/{seed}", "GET")
        return result
    
    def compare(self, data_a: bytes, data_b: bytes, symbol_length_mode: str = "auto_curve") -> Dict[str, Any]:
        """Compare two data items by structural overlap"""
        payload = {
            "data_a_b64": base64.b64encode(data_a).decode('utf-8'),
            "data_b_b64": base64.b64encode(data_b).decode('utf-8'),
            "symbol_length_mode": symbol_length_mode
        }
        
        result = self._request("/v1/compare", "POST", payload)
        return result


# Singleton instance
_ufm_client = None

def get_ufm_client(api_key: Optional[str] = None) -> UFMClient:
    """Get or create UFM client singleton"""
    global _ufm_client
    
    if _ufm_client is None:
        if api_key is None:
            # Default key (user's production key)
            api_key = "ufm_live_8f430fc7.Psl_W4LR5Y_4C1EVmdIgQWrtoNyv65Rx4jvmYW2H2DA"
        
        _ufm_client = UFMClient(api_key)
    
    return _ufm_client


if __name__ == "__main__":
    # Test basic connectivity
    client = get_ufm_client()
    
    print("=" * 60)
    print("UFM CLIENT TEST")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n[1] Health Check")
    health = client.health()
    print(f"Status: {health.get('status')}")
    print(f"Engine version: {health.get('engine_version')}")
    
    # Test 2: Universal process
    print("\n[2] Universal Pipeline Test")
    data = b"Hello World"
    result = client.process_universal(data, verify=True)
    print(f"Success: {result.get('success')}")
    print(f"Quality score: {result.get('quality_score')}")
    print(f"Seed: {result.get('seed')}")
    print(f"Replay valid: {result.get('replay_valid')}")
    print(f"Stages: {result.get('stages_completed')}")
    
    if result.get('principles'):
        print(f"\nPrinciples ({len(result['principles'])} stages):")
        for p in result['principles']:
            print(f"  {p.get('name'):15} ({p.get('symbol')}): weight={p.get('weight')}")
    
    print("\n" + "=" * 60)
    print("UFM CLIENT - READY FOR INTEGRATION")
    print("=" * 60)
