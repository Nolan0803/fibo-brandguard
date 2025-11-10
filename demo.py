"""
Demo Script for FIBO BrandGuard
Demonstrates the core functionality of all modules.
"""

from vlm_agent import VLMAgent
from policy_engine import PolicyEngine
from fibo_client import FIBOClient
from audit_log import AuditLog
import json


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def main():
    """Run the demo."""
    print("\n🛡️  FIBO BrandGuard Demo\n")
    
    # Initialize components
    print_section("Initializing Components")
    vlm_agent = VLMAgent()
    policy_engine = PolicyEngine("brand_profile.json")
    fibo_client = FIBOClient()
    audit_log = AuditLog("demo_audit_log.json")
    
    print("✓ VLM Agent initialized")
    print("✓ Policy Engine initialized")
    print("✓ FIBO Client initialized")
    print("✓ Audit Log initialized")
    
    # Display brand policies
    print_section("Brand Policies")
    policy_summary = policy_engine.get_policy_summary()
    print(f"Brand: {policy_summary['brand_name']}")
    print(f"\nAllowed Themes: {', '.join(policy_summary['policies']['allowed_themes'])}")
    print(f"Prohibited Content: {', '.join(policy_summary['policies']['prohibited_content'])}")
    print(f"Color Preferences: {', '.join(policy_summary['policies']['color_preferences'])}")
    
    # Create a sample prompt
    print_section("Creating JSON Prompt")
    prompt = vlm_agent.create_prompt(
        scene_description="A modern professional office workspace with natural lighting and greenery",
        style="photorealistic",
        modifiers=["high quality", "professional", "clean"],
        colors=["blue", "white", "green"],
        elements=["desk", "laptop", "plants"]
    )
    print("Prompt created:")
    print(json.dumps(prompt, indent=2))
    
    # Validate prompt against policies
    print_section("Policy Validation")
    is_valid, violations, warnings = policy_engine.validate_prompt(prompt)
    
    print(f"Validation Result: {'✅ PASSED' if is_valid else '❌ FAILED'}")
    
    if violations:
        print("\nViolations:")
        for v in violations:
            print(f"  ✗ {v}")
    
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  ⚠ {w}")
    
    if not violations and not warnings:
        print("\n✓ No violations or warnings found!")
    
    # Log the request
    policy_decision = {
        "is_valid": is_valid,
        "violations": violations,
        "warnings": warnings
    }
    
    entry_id = audit_log.log_generation_request(
        prompt,
        policy_decision,
        user="demo_user"
    )
    
    print(f"\n✓ Request logged with ID: {entry_id}")
    
    # Generate images (simulated)
    if is_valid:
        print_section("Generating Images")
        print("Generating 4 image variants...")
        
        results = fibo_client.generate_images(prompt, num_variants=4)
        
        print(f"\n✓ Successfully generated {len(results)} variants")
        
        for result in results:
            print(f"\n  Variant {result['variant_id']}:")
            print(f"    Status: {result['status']}")
            print(f"    Model: {result['metadata']['model']}")
            print(f"    Steps: {result['metadata']['steps']}")
        
        # Log results
        audit_log.log_generation_result(entry_id, results)
    
    # Display audit statistics
    print_section("Audit Statistics")
    stats = audit_log.get_statistics()
    
    print(f"Total Entries: {stats['total_entries']}")
    print(f"Generation Requests: {stats['generation_requests']}")
    print(f"Approved Requests: {stats['approved_requests']}")
    print(f"Rejected Requests: {stats['rejected_requests']}")
    print(f"Policy Violations: {stats['policy_violations']}")
    print(f"Approval Rate: {stats['approval_rate']:.1f}%")
    
    # Test with a violating prompt
    print_section("Testing Policy Violation")
    bad_prompt = vlm_agent.create_prompt(
        scene_description="A violent scene with political controversy",
        style="artistic",
        modifiers=["inappropriate"]
    )
    
    print("Testing prompt with prohibited content:")
    print(json.dumps(bad_prompt, indent=2))
    
    is_valid, violations, warnings = policy_engine.validate_prompt(bad_prompt)
    
    print(f"\nValidation Result: {'✅ PASSED' if is_valid else '❌ FAILED'}")
    
    if violations:
        print("\nViolations detected:")
        for v in violations:
            print(f"  ✗ {v}")
        
        # Log violation
        audit_log.log_policy_violation(bad_prompt, violations, user="demo_user")
        print("\n✓ Violation logged to audit trail")
    
    # Final statistics
    print_section("Final Audit Statistics")
    stats = audit_log.get_statistics()
    
    print(f"Total Entries: {stats['total_entries']}")
    print(f"Generation Requests: {stats['generation_requests']}")
    print(f"Approved Requests: {stats['approved_requests']}")
    print(f"Rejected Requests: {stats['rejected_requests']}")
    print(f"Policy Violations: {stats['policy_violations']}")
    print(f"Approval Rate: {stats['approval_rate']:.1f}%")
    
    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60 + "\n")
    print("To run the full Streamlit app, use:")
    print("  streamlit run app.py\n")


if __name__ == "__main__":
    main()
