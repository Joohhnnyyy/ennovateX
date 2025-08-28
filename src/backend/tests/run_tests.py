#!/usr/bin/env python3
"""Test runner script for EnnovateX AI Platform.

This script provides various options for running tests with different configurations.
"""

import sys
import subprocess
import argparse
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle the output."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {description}:")
        print(f"Return code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run tests for EnnovateX AI Platform")
    
    # Test selection options
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--routes", action="store_true", help="Run route tests only")
    parser.add_argument("--services", action="store_true", help="Run service tests only")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--performance", action="store_true", help="Run performance tests only")
    
    # Coverage options
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage report")
    parser.add_argument("--coverage-html", action="store_true", help="Generate HTML coverage report")
    
    # Output options
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--quiet", "-q", action="store_true", help="Quiet output")
    parser.add_argument("--no-header", action="store_true", help="Disable pytest header")
    
    # Parallel execution
    parser.add_argument("--parallel", "-n", type=int, help="Number of parallel workers")
    
    # Specific test file or pattern
    parser.add_argument("--file", help="Run specific test file")
    parser.add_argument("--pattern", "-k", help="Run tests matching pattern")
    
    # Debugging options
    parser.add_argument("--pdb", action="store_true", help="Drop into debugger on failures")
    parser.add_argument("--lf", action="store_true", help="Run last failed tests only")
    parser.add_argument("--ff", action="store_true", help="Run failed tests first")
    
    # Environment options
    parser.add_argument("--env", choices=["test", "dev", "prod"], default="test", 
                       help="Environment to run tests in")
    
    args = parser.parse_args()
    
    # Set up environment
    os.environ["ENVIRONMENT"] = args.env
    os.environ["TESTING"] = "true"
    
    # Change to the backend directory
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)
    
    # Build base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add test selection
    if args.all or not any([args.routes, args.services, args.unit, args.integration, args.performance]):
        cmd.append("tests/")
    else:
        if args.routes:
            cmd.extend(["tests/test_routes_*.py"])
        if args.services:
            cmd.extend(["tests/test_services_*.py"])
        if args.unit:
            cmd.extend(["-m", "not integration and not performance"])
        if args.integration:
            cmd.extend(["-m", "integration"])
        if args.performance:
            cmd.extend(["-m", "performance"])
    
    # Add specific file or pattern
    if args.file:
        cmd.append(f"tests/{args.file}")
    
    if args.pattern:
        cmd.extend(["-k", args.pattern])
    
    # Add coverage options
    if args.coverage or args.coverage_html:
        cmd.extend(["--cov=app", "--cov-report=term-missing"])
        if args.coverage_html:
            cmd.extend(["--cov-report=html:htmlcov"])
    
    # Add output options
    if args.verbose:
        cmd.append("-v")
    elif args.quiet:
        cmd.append("-q")
    
    if args.no_header:
        cmd.append("--no-header")
    
    # Add parallel execution
    if args.parallel:
        cmd.extend(["-n", str(args.parallel)])
    
    # Add debugging options
    if args.pdb:
        cmd.append("--pdb")
    if args.lf:
        cmd.append("--lf")
    if args.ff:
        cmd.append("--ff")
    
    # Add common options
    cmd.extend([
        "--tb=short",  # Shorter traceback format
        "--strict-markers",  # Strict marker checking
        "--disable-warnings",  # Disable warnings for cleaner output
    ])
    
    # Print configuration
    print(f"\n{'='*60}")
    print("EnnovateX AI Platform Test Runner")
    print(f"{'='*60}")
    print(f"Environment: {args.env}")
    print(f"Working Directory: {os.getcwd()}")
    print(f"Python Path: {sys.executable}")
    
    # Check if pytest is available
    try:
        subprocess.run(["python", "-m", "pytest", "--version"], 
                      capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("Error: pytest is not installed. Please install it with:")
        print("pip install pytest pytest-asyncio pytest-cov")
        return 1
    
    # Run the tests
    success = run_command(cmd, "Running tests")
    
    if args.coverage_html and success:
        print(f"\n{'='*60}")
        print("Coverage report generated in htmlcov/index.html")
        print(f"{'='*60}")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())