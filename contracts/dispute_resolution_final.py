# { "Depends": "py-genlayer:test" }
from genlayer import *
import json


class DisputeResolution(gl.Contract):
    """
    AI-Powered Dispute Resolution System
    Supports multiple cases with AI consensus
    """
    
    # Store cases as list of dictionaries
    cases: list
    
    def __init__(self):
        self.cases = []
    
    @gl.public.write
    def create_case(self, plaintiff: str, defendant: str) -> None:
        """Create a new dispute case"""
        new_case = {
            "plaintiff": plaintiff,
            "defendant": defendant,
            "plaintiff_evidence": "",
            "defendant_evidence": "",
            "status": "awaiting_evidence",
            "winner": "",
            "reasoning": ""
        }
        self.cases.append(new_case)
    
    @gl.public.write
    def submit_evidence(self, case_id: int, party: str, evidence: str) -> None:
        """Submit evidence for plaintiff or defendant"""
        if case_id >= len(self.cases):
            return
        
        case = self.cases[case_id]
        
        if party == "plaintiff":
            case["plaintiff_evidence"] = evidence
        elif party == "defendant":
            case["defendant_evidence"] = evidence
        
        # Update status if both parties submitted
        if case["plaintiff_evidence"] and case["defendant_evidence"]:
            case["status"] = "ready_for_resolution"
    
    @gl.public.write
    def resolve_case(self, case_id: int) -> None:
        """AI analyzes evidence and determines winner"""
        if case_id >= len(self.cases):
            return
        
        case = self.cases[case_id]
        
        # Extract data before non-deterministic execution
        p_name = case["plaintiff"]
        d_name = case["defendant"]
        p_evidence = case["plaintiff_evidence"]
        d_evidence = case["defendant_evidence"]
        
        def analyze_dispute() -> str:
            prompt = f"""You are an impartial AI judge analyzing a dispute between two parties.

CASE DETAILS:
Plaintiff: {p_name}
Plaintiff's Evidence: {p_evidence}

Defendant: {d_name}
Defendant's Evidence: {d_evidence}

TASK:
Analyze both sides objectively. Consider:
1. Strength and credibility of evidence
2. Logical consistency of arguments
3. Fairness and reasonableness of claims
4. Patterns of good faith or bad faith

Determine who has the stronger case.

RESPONSE FORMAT (must be valid JSON):
{{
    "winner": "plaintiff" or "defendant",
    "reasoning": "Your brief explanation (2-3 sentences)"
}}

Return ONLY the JSON object. No markdown formatting, no additional text."""
            
            result = gl.nondet.exec_prompt(prompt)
            # Clean any markdown artifacts
            result = result.replace("```json", "").replace("```", "").strip()
            return result
        
        # Use equivalence principle for AI consensus
        result = gl.eq_principle.prompt_non_comparative(
            analyze_dispute,
            task="Analyze dispute evidence and determine the winner",
            criteria="Must return valid JSON with 'winner' (plaintiff/defendant) and 'reasoning' fields"
        )
        
        # Parse and update case
        try:
            decision = json.loads(result)
            case["winner"] = decision.get("winner", "")
            case["reasoning"] = decision.get("reasoning", "")
            case["status"] = "resolved"
        except:
            case["status"] = "error"
            case["reasoning"] = "Failed to parse AI decision"
    
    @gl.public.view
    def get_case(self, case_id: int) -> dict:
        """Retrieve specific case details"""
        if case_id >= len(self.cases):
            return {}
        
        case = self.cases[case_id]
        return {
            "case_id": case_id,
            "plaintiff": case["plaintiff"],
            "defendant": case["defendant"],
            "plaintiff_evidence": case["plaintiff_evidence"],
            "defendant_evidence": case["defendant_evidence"],
            "status": case["status"],
            "winner": case["winner"],
            "reasoning": case["reasoning"]
        }
    
    @gl.public.view
    def get_all_cases(self) -> dict:
        """Retrieve all cases"""
        all_cases = []
        for i in range(len(self.cases)):
            case = self.cases[i]
            all_cases.append({
                "case_id": i,
                "plaintiff": case["plaintiff"],
                "defendant": case["defendant"],
                "status": case["status"],
                "winner": case["winner"]
            })
        
        return {
            "total": len(self.cases),
            "cases": all_cases
        }
    
    @gl.public.view
    def get_case_count(self) -> int:
        """Get total number of cases"""
        return len(self.cases)
