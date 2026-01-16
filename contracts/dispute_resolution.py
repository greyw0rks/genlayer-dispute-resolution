# { "Depends": "py-genlayer:test" }

from genlayer import *

@allow_storage
class DisputeCase:
    plaintiff: str
    defendant: str
    plaintiff_evidence: str
    defendant_evidence: str
    resolved: bool
    winner: str
    reasoning: str
    
    def __init__(
        self,
        plaintiff: str = "",
        defendant: str = "",
        plaintiff_evidence: str = "",
        defendant_evidence: str = "",
        resolved: bool = False,
        winner: str = "",
        reasoning: str = ""
    ):
        self.plaintiff = plaintiff
        self.defendant = defendant
        self.plaintiff_evidence = plaintiff_evidence
        self.defendant_evidence = defendant_evidence
        self.resolved = resolved
        self.winner = winner
        self.reasoning = reasoning

class Contract(gl.Contract):
    cases: TreeMap[u256, DisputeCase]
    case_counter: u256

    def __init__(self):
        self.cases = TreeMap[u256, DisputeCase]()
        self.case_counter = u256(0)

    @gl.public.write
    def create_case(self, plaintiff: str, defendant: str):
        """Create a new dispute case"""
        case_id = self.case_counter
        self.cases[case_id] = DisputeCase(
            plaintiff=plaintiff,
            defendant=defendant,
            plaintiff_evidence="",
            defendant_evidence="",
            resolved=False,
            winner="",
            reasoning=""
        )
        self.case_counter += u256(1)

    @gl.public.write
    def submit_evidence(self, case_id: int, party: str, evidence: str):
        """Submit evidence for a case"""
        case = self.cases.get(u256(case_id))
        if not case:
            raise Exception("Case not found")
        
        if case.resolved:
            raise Exception("Case already resolved")

        if party == "plaintiff":
            case.plaintiff_evidence = evidence
        elif party == "defendant":
            case.defendant_evidence = evidence
        else:
            raise Exception("Invalid party")

    @gl.public.write
    def resolve_case(self, case_id: int):
        """Resolve dispute using AI analysis"""
        case = self.cases.get(u256(case_id))
        if not case:
            raise Exception("Case not found")
        
        if case.resolved:
            raise Exception("Case already resolved")

        if not case.plaintiff_evidence or not case.defendant_evidence:
            raise Exception("Both parties must submit evidence")

        # Extract data BEFORE nondet block
        plaintiff_name = case.plaintiff
        defendant_name = case.defendant
        plaintiff_ev = case.plaintiff_evidence
        defendant_ev = case.defendant_evidence

        def analyze_dispute():
            prompt = f"""
            Analyze this dispute and determine the winner based on evidence quality.
            
            Plaintiff ({plaintiff_name}):
            {plaintiff_ev}
            
            Defendant ({defendant_name}):
            {defendant_ev}
            
            Respond with a JSON object:
            {{
                "winner": "plaintiff" or "defendant",
                "reasoning": "brief explanation"
            }}
            """
            result = gl.nondet.exec_prompt(prompt)
            # Clean up potential markdown formatting
            result = result.replace("```json", "").replace("```", "").strip()
            return result

        result = gl.eq_principle.prompt_non_comparative(
            analyze_dispute,
            task="Analyze dispute evidence and determine winner",
            criteria="Response must be valid JSON with winner (plaintiff/defendant) and reasoning fields"
        )

        import json
        decision = json.loads(result)
        
        case.resolved = True
        case.winner = decision["winner"]
        case.reasoning = decision["reasoning"]

    @gl.public.view
    def get_case(self, case_id: int) -> dict:
        """Retrieve case details"""
        case = self.cases.get(u256(case_id))
        if not case:
            return {}
        
        return {
            "plaintiff": case.plaintiff,
            "defendant": case.defendant,
            "plaintiff_evidence": case.plaintiff_evidence,
            "defendant_evidence": case.defendant_evidence,
            "resolved": case.resolved,
            "winner": case.winner,
            "reasoning": case.reasoning
        }

    @gl.public.view
    def get_all_cases(self) -> list[dict]:
        """Get all cases"""
        all_cases = []
        for case_id in range(int(self.case_counter)):
            case_data = self.get_case(case_id)
            if case_data:
                all_cases.append(case_data)
        return all_cases
