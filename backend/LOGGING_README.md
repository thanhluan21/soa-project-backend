# Logging System Documentation

## Tổng quan

Hệ thống logging được thiết kế để ghi lại các hoạt động của ứng dụng với 4 levels: DEBUG, INFO, WARNING, ERROR.

## Cấu hình

### Environment Variables
- `LOG_LEVEL`: Thiết lập mức độ log (DEBUG, INFO, WARNING, ERROR)
- `LOG_TO_STDOUT`: Ghi log ra stdout (true/false)

### Cấu hình theo môi trường
- **Development**: DEBUG level, ghi vào file và console
- **Testing**: WARNING level
- **Production**: ERROR level, chỉ ghi ra stdout

## Cách sử dụng

### 1. Import logger
```python
from project.logger import get_logger

# Tạo logger cho module hiện tại
logger = get_logger('module_name')
```

### 2. Sử dụng các logging levels

```python
# DEBUG - thông tin chi tiết cho debugging
logger.debug("Detailed debug information")

# INFO - thông tin chung về hoạt động của app
logger.info("User logged in successfully")

# WARNING - cảnh báo về vấn đề có thể xảy ra
logger.warning("Database connection slow")

# ERROR - lỗi nghiêm trọng
logger.error("Failed to process request")

# EXCEPTION - ghi lỗi với full traceback
try:
    # some code
    pass
except Exception as e:
    logger.exception("Error occurred during processing")
```

### 3. Structured logging
```python
user_id = 123
action = "login"

logger.info(f"User {user_id} attempting {action}")
logger.error(f"Error during {action} for user {user_id}: {error_message}")
```

## File logs

Logs được lưu trong thư mục `services/backend/logs/`:
- `app.log`: Tất cả logs từ INFO trở lên
- `error.log`: Chỉ ERROR logs
- Log rotation: 10MB per file, giữ 5 backup files

## Request Logging

Tự động log tất cả HTTP requests:
- Request start: method, URL
- Request completion: status code, duration
- Debug mode: headers và request/response data
- Error handling: unhandled exceptions

## Models Logging

Logging cho database operations:
- **User operations**: creation, lookup, status changes, admin privileges
- **Exercise operations**: creation, JSON conversion
- **Score operations**: creation, updates, JSON conversion
- **Token operations**: encoding, decoding, expiration
- **Database transactions**: commits, rollbacks, errors

## Ví dụ sử dụng

### General logging
Xem file `project/logger_example.py` để biết cách sử dụng chi tiết.

```bash
cd services/backend
python -m project.logger_example
```

### Auth module logging
Xem file `project/auth_logging_demo.py` để biết cách logging trong authentication.

```bash
cd services/backend
python -m project.auth_logging_demo
```

### Models logging
Xem file `project/models_logging_demo.py` để biết cách logging trong database models.

```bash
cd services/backend
python -m project.models_logging_demo
```

### Test models với logging thực tế
```bash
cd services/backend
python -m project.test_models_logging
```

### Test JWT token operations
```bash
cd services/backend
python test_token_simple.py        # Basic token test
python test_token_edge_cases.py    # Edge cases and error scenarios
```

## Best Practices

1. **Sử dụng đúng level**:
   - DEBUG: Chi tiết kỹ thuật, token validation
   - INFO: Hoạt động bình thường (login, logout, registration)
   - WARNING: Vấn đề bảo mật (failed login, invalid tokens)
   - ERROR: Lỗi nghiêm trọng (database errors, system failures)

2. **Structured logging**:
   ```python
   logger.info(f"User {user_id} performed {action} on {resource}")
   logger.warning(f"Failed login attempt for email: {email}")
   ```

3. **Không log sensitive data**:
   ```python
   # Tránh
   logger.info(f"User password: {password}")
   logger.debug(f"Auth token: {token}")
   
   # Nên
   logger.info(f"User {username} authentication attempt")
   logger.debug("Token successfully validated")
   ```

4. **Security logging**:
   ```python
   logger.warning(f"Multiple failed login attempts for: {email}")
   logger.error("Potential brute force attack detected")
   logger.info(f"User {username} logged in successfully")
   ```

5. **Database operations logging**:
   ```python
   logger.info(f"Creating new user: {username} ({email})")
   logger.debug(f"Encoding auth token for user_id: {user_id}")
   logger.warning("Auth token expired")
   logger.error(f"Failed to create user {username}: {str(e)}")
   ```

6. **Sử dụng exception() cho errors**:
   ```python
   try:
       # code
   except Exception as e:
       logger.exception("Error processing request")  # Tự động include traceback
   ```

## Monitoring

Trong production, có thể tích hợp với:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Fluentd
- CloudWatch (AWS)
- Stackdriver (GCP)

## Troubleshooting

1. **Logs không xuất hiện**: Kiểm tra LOG_LEVEL environment variable
2. **File permission errors**: Đảm bảo thư mục logs có quyền write
3. **Log files quá lớn**: Log rotation tự động hoạt động ở 10MB