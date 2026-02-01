# { "Depends": "py-genlayer:test" }
from genlayer import *
import json
import typing


class DisputeResolution(gl.Contract):
    """
    AI-Powered Dispute Resolution System
    Supports multiple cases with AI consensus
    """
    
    # Store cases using TreeMap (GenLayer's dict equivalent)
    cases: TreeMap[u256, str]  # case_id -> JSON string of case data
    case_count: u256
    
    def __init__(self):
        self.case_count = u256(0)
    
    @gl.public.write
    def create_case(self, plaintiff: str, defendant: str) -> None:
        """Create a new dispute case"""
        case_id = self.case_count
        
        case_data = {
            "plaintiff": plaintiff,
            "defendant": defendant,
            "plaintiff_evidence": "",
            "defendant_evidence": "",
            "status": "awaiting_evidence",
            "winner": "",
            "reasoning": ""
        }
        
        # Store as JSON string
        self.cases[case_id] = json.dumps(case_data)
        self.case_count = u256(int(self.case_count) + 1)
    
    @gl.public.write
    def submit_evidence(self, case_id: int, party: str, evidence: str) -> None:
        """Submit evidence for plaintiff or defendant"""
        case_key = u256(case_id)
        case_json = self.cases.get(case_key, None)
        
        if case_json is None:
            return
        
        case = json.loads(case_json)
        
        if party == "plaintiff":
            case["plaintiff_evidence"] = evidence
        elif party == "defendant":
            case["defendant_evidence"] = evidence
        
        # Update status if both parties submitted
        if case["plaintiff_evidence"] and case["defendant_evidence"]:
            case["status"] = "ready_for_resolution"
        
        # Save back
        self.cases[case_key] = json.dumps(case)
    
    @gl.public.write
    def resolve_case(self, case_id: int) -> None:
        """AI analyzes evidence and determines winner"""
        case_key = u256(case_id)
        case_json = self.cases.get(case_key, None)
        
        if case_json is None:
            return
        
        case = json.loads(case_json)
        
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
        
        # Save back
        self.cases[case_key] = json.dumps(case)
    
    @gl.public.view
    def get_case(self, case_id: int) -> typing.Any:
        """Retrieve specific case details"""
        case_key = u256(case_id)
        case_json = self.cases.get(case_key, None)
        
        if case_json is None:
            return {}
        
        case = json.loads(case_json)
        case["case_id"] = case_id
        return case
    
    @gl.public.view
    def get_all_cases(self) -> typing.Any:
        """Retrieve all cases"""
        all_cases = []
        
        for i in range(int(self.case_count)):
            case_json = self.cases.get(u256(i), None)
            if case_json is not None:
                case = json.loads(case_json)
                all_cases.append({
                    "case_id": i,
                    "plaintiff": case["plaintiff"],
                    "defendant": case["defendant"],
                    "status": case["status"],
                    "winner": case["winner"]
                })
        
        return {
            "total": int(self.case_count),
            "cases": all_cases
        }
    
    @gl.public.view
    def get_case_count(self) -> int:
        """Get total number of cases"""
        return int(self.case_count)
