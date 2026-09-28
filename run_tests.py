import subprocess
import sys
import time

def run_suite():
    print("=" * 65)
    print("FLOWGENIE TEST SUITE RUNNER")
    print("=" * 65)

    test_files = [
        "tests/test_auth_system.py",
        "tests/test_landing_auth_gate.py",
        "tests/test_unique_vendors.py",
        "tests/test_custom_category.py",
        "tests/test_custom_schedule.py",
        "tests/test_timing_features.py",
        "tests/test_personalization.py",
        "tests/test_automation_systems.py",
        "tests/test_agent_evaluation.py",
        "tests/test_full_flow.py",
    ]

    all_passed = True
    for test in test_files:
        print(f"\n[RUNNING] {test}...")
        res = subprocess.run([sys.executable, test])
        if res.returncode == 0:
            print(f"  --> PASSED [OK]: {test}")
        else:
            print(f"  --> FAILED [ERR]: {test} (Exit code {res.returncode})")
            all_passed = False

    print("\n" + "=" * 65)
    if all_passed:
        print("ALL TESTS IN SUITE PASSED SUCCESSFULLY! [OK]")
    else:
        print("SOME TESTS FAILED! CHECK OUTPUT ABOVE.")
    print("=" * 65)

if __name__ == "__main__":
    run_suite()
