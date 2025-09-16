#!/usr/bin/env python3
"""
Script to remove duplicate models from LiteLLM proxy
Usage: python3 cleanup_duplicates.py --ollama-url http://192.168.1.250:11434 --litellm-url http://localhost:4000 --api-key your-key
"""

import requests
import json
import argparse
import sys
from collections import defaultdict

def parse_arguments():
    parser = argparse.ArgumentParser(description='Remove duplicate models from LiteLLM proxy')
    parser.add_argument('--ollama-url', required=True, 
                       help='Ollama server URL (e.g., http://192.168.1.250:11434)')
    parser.add_argument('--litellm-url', required=True,
                       help='LiteLLM proxy URL (e.g., http://localhost:4000)')
    parser.add_argument('--api-key', required=True,
                       help='LiteLLM API key/master key')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be deleted without actually deleting')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Clean URLs (remove trailing slashes)
    ollama_url = args.ollama_url.rstrip('/')
    litellm_url = args.litellm_url.rstrip('/')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {args.api_key}"
    }
    
    print(f"Connecting to LiteLLM at: {litellm_url}")
    print(f"Ollama server: {ollama_url}")
    print(f"Dry run mode: {args.dry_run}")
    print("-" * 50)
    
    # Get all models from LiteLLM
    try:
        response = requests.get(f"{litellm_url}/model/info", headers=headers)
        if response.status_code != 200:
            print(f"Failed to get models: {response.status_code} - {response.text}")
            sys.exit(1)
        
        models_data = response.json()
        models = models_data['data']
        print(f"Total models found: {len(models)}")
        
    except Exception as e:
        print(f"Error connecting to LiteLLM: {e}")
        sys.exit(1)
    
    # Group models by name to find duplicates
    model_groups = defaultdict(list)
    for model in models:
        model_name = model.get('model_name', '')
        model_id = model.get('model_info', {}).get('id', '')
        
        model_groups[model_name].append({
            'id': model_id, 
            'model_name': model_name,
            'full_data': model
        })
    
    # Find and process duplicates
    total_duplicates = 0
    removed_count = 0
    
    for model_name, model_list in model_groups.items():
        if len(model_list) > 1:
            total_duplicates += len(model_list) - 1
            print(f"\nFound {len(model_list)} copies of '{model_name}'")
            
            # Keep the first one, remove/show the rest
            for i, model_info in enumerate(model_list[1:], 1):
                model_id = model_info['id']
                if model_id:
                    if args.dry_run:
                        print(f"  [DRY RUN] Would remove duplicate #{i}: {model_id}")
                        removed_count += 1
                    else:
                        # Actually delete the duplicate
                        try:
                            delete_response = requests.delete(
                                f"{litellm_url}/model/delete",
                                headers=headers,
                                data=json.dumps({"id": model_id})
                            )
                            
                            if delete_response.status_code in [200, 204]:
                                print(f"  ✓ Removed duplicate #{i}: {model_id}")
                                removed_count += 1
                            else:
                                print(f"  ✗ Failed to remove {model_id}: {delete_response.status_code} - {delete_response.text}")
                        except Exception as e:
                            print(f"  ✗ Error removing {model_id}: {e}")
                else:
                    print(f"  ✗ No ID found for duplicate #{i}")
    
    print(f"\n" + "=" * 50)
    if args.dry_run:
        print(f"DRY RUN SUMMARY:")
        print(f"Found {total_duplicates} duplicate models")
        print(f"Would remove {removed_count} duplicates")
        print(f"\nRun without --dry-run to actually delete the duplicates")
    else:
        print(f"SUMMARY:")
        print(f"Found {total_duplicates} duplicate models")
        print(f"Successfully removed {removed_count} duplicates")

if __name__ == "__main__":
    main()