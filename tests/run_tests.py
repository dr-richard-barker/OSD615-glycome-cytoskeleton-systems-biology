#!/usr/bin/env python3
"""
run_tests.py
Automated test runner executing all unit and integration tests across tests/
Compatible with standard library and virtualenv.
"""

import os
import sys
import inspect
import importlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(BASE_DIR, 'tests')
sys.path.insert(0, BASE_DIR)

TEST_MODULES = [
    'test_data_integrity',
    'test_analysis_pipelines',
    'test_json_schemas',
    'test_fair_compliance'
]

def main():
    print("=" * 65)
    print("  OSD-615 Systems Biology Project — Automated Test Suite")
    print("=" * 65)
    
    total = 0
    passed = 0
    failed = 0
    failures = []

    for mod_name in TEST_MODULES:
        print(f"\n[RUNNING] tests/{mod_name}.py")
        try:
            mod = importlib.import_module(f"tests.{mod_name}")
        except Exception as e:
            print(f"  ❌ FAILED TO IMPORT {mod_name}: {e}")
            failed += 1
            failures.append((f"{mod_name} (import)", str(e)))
            continue

        test_funcs = [
            (name, func) for name, func in inspect.getmembers(mod, inspect.isfunction)
            if name.startswith('test_')
        ]

        for name, func in test_funcs:
            total += 1
            try:
                func()
                print(f"  ✓ {name}")
                passed += 1
            except Exception as e:
                print(f"  ✗ {name}: {e}")
                failed += 1
                failures.append((f"{mod_name}.{name}", str(e)))

    print("\n" + "=" * 65)
    print(f"RESULTS: {passed}/{total} Passed | {failed} Failed")
    print("=" * 65)

    if failures:
        print("\nFAILURES:")
        for name, err in failures:
            print(f"  - {name}: {err}")
        sys.exit(1)
    else:
        print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")
        sys.exit(0)

if __name__ == '__main__':
    main()
