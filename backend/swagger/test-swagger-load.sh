#!/bin/bash

echo "🧪 Testing Swagger JSON Loading..."

# Build the container
echo "1. Building Swagger UI container..."
docker build -f Dockerfile-dev -t swagger-test . > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Failed to build container"
    exit 1
fi

# Run container
echo "2. Starting container..."
docker run -d --name swagger-test -p 8081:8080 swagger-test > /dev/null 2>&1

# Wait for container to start
echo "3. Waiting for container to start..."
sleep 10

# Test if swagger.json is accessible
echo "4. Testing swagger.json accessibility..."
if curl -f -s http://localhost:8081/swagger.json > /dev/null; then
    echo "✅ swagger.json is accessible"
    
    # Get the actual content
    echo "5. Checking swagger.json content..."
    CONTENT=$(curl -s http://localhost:8081/swagger.json)
    
    # Check if it's valid JSON
    if echo "$CONTENT" | jq . > /dev/null 2>&1; then
        echo "✅ swagger.json is valid JSON"
        
        # Check if it contains our API info
        TITLE=$(echo "$CONTENT" | jq -r '.info.title' 2>/dev/null)
        VERSION=$(echo "$CONTENT" | jq -r '.info.version' 2>/dev/null)
        
        if [ "$TITLE" != "null" ] && [ "$TITLE" != "" ]; then
            echo "✅ API Title: $TITLE"
        else
            echo "❌ Missing API title"
        fi
        
        if [ "$VERSION" != "null" ] && [ "$VERSION" != "" ]; then
            echo "✅ API Version: $VERSION"
        else
            echo "❌ Missing API version"
        fi
        
        # Count paths
        PATHS_COUNT=$(echo "$CONTENT" | jq '.paths | length' 2>/dev/null)
        if [ "$PATHS_COUNT" -gt 0 ]; then
            echo "✅ Found $PATHS_COUNT API paths"
        else
            echo "❌ No API paths found"
        fi
        
    else
        echo "❌ swagger.json is not valid JSON"
        echo "Content preview:"
        echo "$CONTENT" | head -5
    fi
    
else
    echo "❌ swagger.json is not accessible"
fi

# Test main Swagger UI page
echo "6. Testing Swagger UI main page..."
if curl -f -s http://localhost:8081/ > /dev/null; then
    echo "✅ Swagger UI main page is accessible"
    
    # Check if the page contains reference to our swagger.json
    PAGE_CONTENT=$(curl -s http://localhost:8081/)
    if echo "$PAGE_CONTENT" | grep -q "swagger.json"; then
        echo "✅ Page references swagger.json"
    else
        echo "⚠️  Page might not be configured to load swagger.json"
    fi
    
else
    echo "❌ Swagger UI main page is not accessible"
fi

# Check container logs for any errors
echo "7. Checking container logs..."
LOGS=$(docker logs swagger-test 2>&1)

if echo "$LOGS" | grep -q "✅.*loaded successfully"; then
    echo "✅ Container started successfully"
elif echo "$LOGS" | grep -q "❌"; then
    echo "❌ Found errors in container logs:"
    echo "$LOGS" | grep "❌"
else
    echo "ℹ️  Container logs:"
    echo "$LOGS" | tail -10
fi

# Cleanup
echo "8. Cleaning up..."
docker stop swagger-test > /dev/null 2>&1
docker rm swagger-test > /dev/null 2>&1
docker rmi swagger-test > /dev/null 2>&1

echo "🎉 Swagger JSON loading test completed!"