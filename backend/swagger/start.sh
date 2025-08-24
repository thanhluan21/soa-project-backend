#!/bin/sh

echo "Starting Swagger UI configuration..."
echo "Swagger UI Version: $SWAGGER_UI_VERSION"
echo "API URL: $API_URL"
echo "Custom URL: $URL"

# Force use local swagger.json file
SWAGGER_URL="./swagger.json"
echo "🎯 Forcing local swagger.json file: $SWAGGER_URL"

# Override any URL environment variables to use local file
if [ "$URL" != "**None**" ] && [ -n "$URL" ]; then
    echo "ℹ️  Ignoring custom URL ($URL) - using local file instead"
fi

# Check if swagger.json exists
if [ -f "/usr/share/nginx/html/swagger.json" ]; then
    echo "✅ Found swagger.json file"
    # Show first few lines for verification
    echo "📄 Swagger spec preview:"
    head -5 /usr/share/nginx/html/swagger.json
else
    echo "❌ swagger.json file not found!"
    ls -la /usr/share/nginx/html/
fi

# Replace the default Petstore URL with our swagger.json
echo "🔧 Configuring Swagger UI to use: $SWAGGER_URL"

# For Swagger UI 5.x, we need to replace the URL in the index.html
sed -i -e 's@https://petstore.swagger.io/v2/swagger.json@'"$SWAGGER_URL"'@g' /usr/share/nginx/html/index.html
sed -i -e 's@http://petstore.swagger.io/v2/swagger.json@'"$SWAGGER_URL"'@g' /usr/share/nginx/html/index.html

# Also replace any other common Swagger demo URLs
sed -i -e 's@https://petstore3.swagger.io/api/v3/openapi.json@'"$SWAGGER_URL"'@g' /usr/share/nginx/html/index.html

# Create a custom initializer script to load LOCAL swagger.json
cat > /usr/share/nginx/html/swagger-initializer.js << 'EOF'
window.onload = function() {
  //<editor-fold desc="Changeable Configuration Block">

  // Force load local swagger.json file
  window.ui = SwaggerUIBundle({
    url: './swagger.json',  // Always use local file
    dom_id: '#swagger-ui',
    deepLinking: true,
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    plugins: [
      SwaggerUIBundle.plugins.DownloadUrl
    ],
    layout: "StandaloneLayout",
    validatorUrl: null,
    tryItOutEnabled: true,
    supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch', 'head', 'options'],
    onComplete: function() {
      console.log('✅ Swagger UI loaded successfully with LOCAL swagger.json');
      console.log('📄 Loaded from: ./swagger.json');
    },
    onFailure: function(data) {
      console.error('❌ Failed to load LOCAL swagger.json:', data);
      console.error('🔍 Check if swagger.json exists and is valid JSON');
      
      // Try to fetch and show the error
      fetch('./swagger.json')
        .then(response => {
          if (!response.ok) {
            console.error('HTTP Error:', response.status, response.statusText);
          }
          return response.text();
        })
        .then(text => {
          console.log('📄 swagger.json content preview:', text.substring(0, 200) + '...');
        })
        .catch(err => {
          console.error('❌ Cannot fetch swagger.json:', err);
        });
    }
  });

  //</editor-fold>
};
EOF

# Replace the default swagger-initializer.js if it exists
if [ -f "/usr/share/nginx/html/swagger-initializer.js.bak" ]; then
    echo "📝 Backing up original swagger-initializer.js"
else
    cp /usr/share/nginx/html/swagger-initializer.js /usr/share/nginx/html/swagger-initializer.js.bak 2>/dev/null || true
fi

# Copy our custom initializer
cp /usr/share/nginx/html/swagger-initializer.js /usr/share/nginx/html/swagger-initializer.js.custom

# Verify the configuration
echo "🔍 Verifying configuration..."
if grep -q "$SWAGGER_URL" /usr/share/nginx/html/swagger-initializer.js; then
    echo "✅ Configuration updated successfully"
else
    echo "❌ Configuration update failed"
fi

# Test nginx configuration
echo "🧪 Testing nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid"
else
    echo "❌ Nginx configuration error"
    exit 1
fi

echo "🚀 Starting Nginx..."
exec nginx -g 'daemon off;'
