#!/usr/bin/env python3

import os
import sys

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from database import get_database

def get_user_input(prompt, default=None):
    """Get user input with optional default value"""
    if default:
        response = input(f"{prompt} [{default}]: ").strip()
        return response if response else default
    return input(f"{prompt}: ").strip()

def main():
    # Get database connection
    collection = get_database()
    
    # Get system ID prefix
    prefix = get_user_input("Enter system ID prefix to match")
    if not prefix:
        print("Error: Prefix cannot be empty")
        sys.exit(1)
    
    # Get field name
    field_name = get_user_input("Enter field name to add/modify")
    if not field_name:
        print("Error: Field name cannot be empty")
        sys.exit(1)
    
    # Get field value
    field_value = get_user_input("Enter value to set")
    
    # Find matching providers
    query = {"system_id": {"$regex": f"^{prefix}"}}
    matching_providers = list(collection.find(query))
    
    if not matching_providers:
        print(f"No providers found with system ID starting with '{prefix}'")
        sys.exit(0)
    
    # Show preview
    print(f"\nFound {len(matching_providers)} matching providers:")
    for provider in matching_providers:
        print(f"- {provider['system_id']}")
    # Confirm changes
    confirm = get_user_input(f"\nSet {field_name} to '{field_value}' for all {len(matching_providers)} matching providers? (y/N)", "N")
    if confirm.lower() != 'y':
        print("Operation cancelled")
        sys.exit(0)
    
    # Execute changes
    result = collection.update_many(
        query,
        {"$set": {field_name: field_value}}
    )
    
    print(f"\nUpdate complete:")
    print(f"- Modified {result.modified_count} documents")
    print(f"- Matched {result.matched_count} documents")

if __name__ == "__main__":
    main()
