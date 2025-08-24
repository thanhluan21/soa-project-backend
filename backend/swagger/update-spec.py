#!/usr/bin/env python3
"""
Update and validate Swagger specification
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def validate_swagger_spec():
    """Validate swagger.json structure and content"""
    
    swagger_file = Path(__file__).parent / 'swagger.json'
    
    try:
        with open(swagger_file, 'r') as f:
            spec = json.load(f)
        
        print(f"✅ Loaded swagger.json successfully")
        print(f"   Title: {spec['info']['title']}")
        print(f"   Version: {spec['info']['version']}")
        print(f"   Paths: {len(spec['paths'])}")
        print(f"   Schemas: {len(spec.get('components', {}).get('schemas', {}))}")
        
        # Validate required fields
        required_fields = ['openapi', 'info', 'paths']
        for field in required_fields:
            if field not in spec:
                print(f"❌ Missing required field: {field}")
                return False
        
        # Validate info section
        info_required = ['title', 'version']
        for field in info_required:
            if field not in spec['info']:
                print(f"❌ Missing required info field: {field}")
                return False
        
        # Validate OpenAPI version
        if not spec['openapi'].startswith('3.'):
            print(f"❌ Unsupported OpenAPI version: {spec['openapi']}")
            return False
        
        # Count endpoints by method
        methods = {}
        for path, path_obj in spec['paths'].items():
            for method in path_obj.keys():
                if method in ['get', 'post', 'put', 'delete', 'patch']:
                    methods[method] = methods.get(method, 0) + 1
        
        print("📊 API Statistics:")
        for method, count in sorted(methods.items()):
            print(f"   {method.upper()}: {count} endpoints")
        
        print("✅ Swagger specification is valid")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in swagger.json: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ swagger.json not found at {swagger_file}")
        return False
    except Exception as e:
        print(f"❌ Error reading swagger.json: {e}")
        return False

def update_server_url(url):
    """Update server URL in swagger.json"""
    
    swagger_file = Path(__file__).parent / 'swagger.json'
    
    try:
        with open(swagger_file, 'r') as f:
            spec = json.load(f)
        
        if 'servers' in spec and len(spec['servers']) > 0:
            old_url = spec['servers'][0]['url']
            spec['servers'][0]['url'] = url
            
            with open(swagger_file, 'w') as f:
                json.dump(spec, f, indent=2)
            
            print(f"✅ Updated server URL: {old_url} → {url}")
        else:
            print("❌ No servers section found in swagger.json")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating server URL: {e}")
        return False

def update_version():
    """Update version in swagger.json"""
    
    swagger_file = Path(__file__).parent / 'swagger.json'
    
    try:
        with open(swagger_file, 'r') as f:
            spec = json.load(f)
        
        # Update version with timestamp
        current_version = spec['info']['version']
        new_version = f"1.0.{datetime.now().strftime('%Y%m%d')}"
        
        if current_version != new_version:
            spec['info']['version'] = new_version
            
            with open(swagger_file, 'w') as f:
                json.dump(spec, f, indent=2)
            
            print(f"✅ Updated version: {current_version} → {new_version}")
        else:
            print(f"ℹ️  Version already up to date: {current_version}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating version: {e}")
        return False

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("🔧 Swagger Specification Tool")
        print("=" * 30)
        print("Usage:")
        print("  python update-spec.py <server_url>     - Update server URL")
        print("  python update-spec.py --validate       - Validate spec")
        print("  python update-spec.py --update-version - Update version")
        print()
        print("Examples:")
        print("  python update-spec.py http://localhost:5001")
        print("  python update-spec.py --validate")
        return False
    
    arg = sys.argv[1]
    
    if arg == '--validate':
        return validate_swagger_spec()
    elif arg == '--update-version':
        return update_version()
    elif arg.startswith('http'):
        return update_server_url(arg)
    else:
        print(f"❌ Unknown argument: {arg}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
