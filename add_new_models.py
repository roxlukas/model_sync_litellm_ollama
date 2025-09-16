#!/usr/bin/env python3
"""
Script to add only new models from Ollama to LiteLLM proxy (avoiding duplicates)
Usage: python3 add_new_models.py --ollama-url http://192.168.1.250:11434 --litellm-url http://localhost:4000 --api-key your-key
"""

import requests
import json
import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description='Add new models from Ollama to LiteLLM proxy')
    parser.add_argument('--ollama-url', required=True, 
                       help='Ollama server URL (e.g., http://192.168.1.250:11434)')
    parser.add_argument('--litellm-url', required=True,
                       help='LiteLLM proxy URL (e.g., http://localhost:4000)')
    parser.add_argument('--api-key', required=True,
                       help='LiteLLM API key/master key')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be added without actually adding')
    parser.add_argument('--force', action='store_true',
                       help='Add all models even if they already exist (will create duplicates)')
    return parser.parse_args()

def get_ollama_models(ollama_url):
    """Get list of models from Ollama server"""
    try:
        response = requests.get(f"{ollama_url}/api/tags")
        if response.status_code == 200:
            return response.json()["models"]
        else:
            print(f"Failed to get Ollama models: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        return None

def get_existing_models(litellm_url, headers):
    """Get list of existing models from LiteLLM proxy"""
    try:
        response = requests.get(f"{litellm_url}/model/info", headers=headers)
        if response.status_code == 200:
            existing_data = response.json()
            return [model.get('model_name', '') for model in existing_data['data']]
        else:
            print(f"Could not fetch existing models: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Error fetching existing models: {e}")
        return []

def add_model_to_litellm(litellm_url, headers, model_name, ollama_url, dry_run=False):
    """Add a single model to LiteLLM proxy"""
    model_config = {
        "model_name": model_name,
        "litellm_params": {
            "model": f"ollama/{model_name}",
            "api_base": ollama_url
        }
    }
    
    if dry_run:
        return True, f"[DRY RUN] Would add {model_name}"
    
    try:
        response = requests.post(
            f"{litellm_url}/model/new",
            headers=headers,
            data=json.dumps(model_config)
        )
        
        if response.status_code in [200, 201]:
            return True, f"Successfully added {model_name}"
        else:
            return False, f"Failed to add {model_name}: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"Error adding {model_name}: {e}"

def main():
    args = parse_arguments()
    
    # Clean URLs (remove trailing slashes)
    ollama_url = args.ollama_url.rstrip('/')
    litellm_url = args.litellm_url.rstrip('/')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {args.api_key}"
    }
    
    print(f"Ollama server: {ollama_url}")
    print(f"LiteLLM proxy: {litellm_url}")
    print(f"Dry run mode: {args.dry_run}")
    print(f"Force mode: {args.force}")
    print("-" * 50)
    
    # Get models from Ollama
    print("Fetching models from Ollama...")
    ollama_models = get_ollama_models(ollama_url)
    if ollama_models is None:
        sys.exit(1)
    
    print(f"Found {len(ollama_models)} models in Ollama:")
    for model in ollama_models:
        print(f"  - {model['name']}")
    
    print(f"\n" + "-" * 50)
    
    # Get existing models from LiteLLM (unless forced)
    existing_model_names = []
    if not args.force:
        print("Checking existing models in LiteLLM...")
        existing_model_names = get_existing_models(litellm_url, headers)
        print(f"Found {len(existing_model_names)} existing models in LiteLLM")
        if existing_model_names:
            print("Existing models:")
            for model_name in existing_model_names:
                print(f"  - {model_name}")
    else:
        print("Force mode enabled - will add all models regardless of existing ones")
    
    print(f"\n" + "-" * 50)
    
    # Process each model
    added_count = 0
    skipped_count = 0
    failed_count = 0
    
    for model in ollama_models:
        model_name = model["name"]
        
        if not args.force and model_name in existing_model_names:
            print(f"⏭️  Skipping {model_name} - already exists")
            skipped_count += 1
            continue
        
        success, message = add_model_to_litellm(litellm_url, headers, model_name, ollama_url, args.dry_run)
        
        if success:
            if args.dry_run:
                print(f"📋 {message}")
            else:
                print(f"✅ {message}")
            added_count += 1
        else:
            print(f"❌ {message}")
            failed_count += 1
    
    # Summary
    print(f"\n" + "=" * 50)
    print(f"SUMMARY:")
    if args.dry_run:
        print(f"Would add: {added_count} models")
    else:
        print(f"Successfully added: {added_count} models")
    print(f"Skipped (already exist): {skipped_count} models")
    if failed_count > 0:
        print(f"Failed: {failed_count} models")
    
    if args.dry_run and added_count > 0:
        print(f"\nRun without --dry-run to actually add the models")

if __name__ == "__main__":
    main()