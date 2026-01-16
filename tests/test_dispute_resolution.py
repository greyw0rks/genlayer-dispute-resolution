from tools.request import (
    create_new_account,
    post_request_localhost,
    payload,
    deploy_intelligent_contract,
    send_transaction,
    call_contract_method
)
from tools.response import has_success_status

def test_dispute_resolution():
    print("Starting dispute resolution test...")
    
    # Setup validators
    print("Setting up validators...")
    setup_response = post_request_localhost(
        payload("sim_createRandomValidators", [5])
    ).json()
    assert has_success_status(setup_response)
    print("✓ Validators created")

    # Create accounts
    plaintiff_account = create_new_account()
    defendant_account = create_new_account()
    print("✓ Accounts created")

    # Deploy contract
    print("Deploying contract...")
    contract_code = open("contracts/dispute_resolution.py", "r").read()
    contract_address, deploy_response = deploy_intelligent_contract(
        plaintiff_account,
        contract_code,
        "{}"
    )
    assert has_success_status(deploy_response)
    print(f"✓ Contract deployed at: {contract_address}")

    # Create case
    print("\nCreating dispute case...")
    create_response = send_transaction(
        plaintiff_account,
        contract_address,
        "create_case",
        ["Alice", "Bob"]
    )
    assert has_success_status(create_response)
    print("✓ Case created")

    # Submit plaintiff evidence
    print("\nSubmitting plaintiff evidence...")
    plaintiff_evidence = """
    I hired Bob to build a website for $5000. 
    We signed a contract on Jan 1, 2025.
    The deadline was Jan 30, 2025.
    Bob delivered the website on Feb 15, 2025 - 15 days late.
    The website has multiple broken features.
    I have screenshots showing the issues.
    """
    
    evidence_response = send_transaction(
        plaintiff_account,
        contract_address,
        "submit_evidence",
        [0, "plaintiff", plaintiff_evidence]
    )
    assert has_success_status(evidence_response)
    print("✓ Plaintiff evidence submitted")

    # Submit defendant evidence
    print("\nSubmitting defendant evidence...")
    defendant_evidence = """
    Alice kept changing requirements after signing.
    I have email records showing 15 major change requests.
    The original contract didn't include these features.
    I delivered everything in the original contract on time.
    The 'broken features' are the new requests that weren't part of the deal.
    """
    
    defendant_evidence_response = send_transaction(
        defendant_account,
        contract_address,
        "submit_evidence",
        [0, "defendant", defendant_evidence]
    )
    assert has_success_status(defendant_evidence_response)
    print("✓ Defendant evidence submitted")

    # Resolve case
    print("\nResolving case (this may take a moment)...")
    resolve_response = send_transaction(
        plaintiff_account,
        contract_address,
        "resolve_case",
        [0]
    )
    assert has_success_status(resolve_response)
    print("✓ Case resolved")

    # Get case result
    print("\nFetching case result...")
    result = call_contract_method(
        contract_address,
        plaintiff_account,
        "get_case",
        [0]
    )
    assert has_success_status(result)
    
    case_data = result["result"]["data"]
    print("\n" + "="*50)
    print("CASE RESOLUTION")
    print("="*50)
    print(f"Winner: {case_data['winner']}")
    print(f"Reasoning: {case_data['reasoning']}")
    print("="*50)

    # Cleanup
    print("\nCleaning up...")
    post_request_localhost(payload("sim_deleteAllValidators"))
    print("✓ Test complete!")

if __name__ == "__main__":
    test_dispute_resolution()
