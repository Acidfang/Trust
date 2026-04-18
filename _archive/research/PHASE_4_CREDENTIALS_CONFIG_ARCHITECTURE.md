# Phase 4D: Credentials & Configuration Management

**Status**: Design Phase (for review and approval)  
**Scope**: API keys, credentials, environment configuration  
**Priority**: Critical (security, deployment flexibility)

---

## 1. Configuration Layers

### Layer 1: Defaults (Hardcoded)
```python
# config.py - Application defaults
DEFAULT_CONFIG = {
    'api_port': 5000,
    'api_workers': 4,
    'cache_ttl': 3600,
    'db_pool_size': 20,
    'log_level': 'info',
    'platforms': ['twitter', 'reddit', 'mastodon', 'linkedin', 'discord', 'hackernews']
}
```

### Layer 2: Environment Variables (.env)
```bash
# .env (local development)
FLASK_ENV=development
LOG_LEVEL=debug
DATABASE_URL=postgresql://tracker:dev_password@localhost:5432/tracker

# .env.production (deployed)
FLASK_ENV=production
LOG_LEVEL=info
DATABASE_URL=postgresql://tracker:prod_password@postgres:5432/tracker
```

### Layer 3: Configuration Files
```toml
# ~/.tracker/config.toml (user's home directory)
[api]
endpoint = "http://localhost:5000"
timeout = 30
retry_count = 3

[logging]
level = "info"
format = "json"

[cache]
enabled = true
ttl_hours = 1
```

### Layer 4: Secrets Management
```bash
# Option A: Docker Secrets (Swarm/Kubernetes)
/run/secrets/db_password
/run/secrets/twitter_bearer_token
/run/secrets/reddit_client_id

# Option B: HashiCorp Vault (Enterprise)
vault kv get secret/tracker/database_url
vault kv get secret/tracker/twitter_bearer_token

# Option C: AWS Secrets Manager (AWS)
aws secretsmanager get-secret-value --secret-id tracker/database_url

# Option D: Azure Key Vault (Azure)
az keyvault secret show --vault-name tracker-secrets --name database-url
```

### Configuration Precedence (Later Wins)
```
1. Defaults (hardcoded)
2. Environment variables (.env)
3. Config file (config.toml)
4. Secrets manager (vault/aws/azure)
5. CLI flags (--api-key, --debug)
```

---

## 2. Secrets Management Architecture

### Development Environment

**File: .env.local** (Git-ignored)
```bash
# API Credentials
TWITTER_BEARER_TOKEN=AAAABbbwbbb...
TWITTER_API_KEY=xxx
TWITTER_API_SECRET=yyy

REDDIT_CLIENT_ID=abc123xyz
REDDIT_CLIENT_SECRET=def456uvw

MASTODON_TOKEN=ghi789rst
DISCORD_BOT_TOKEN=jkl012mno

LINKEDIN_BEARER_TOKEN=pqr345stu

# Database
DATABASE_URL=postgresql://tracker:dev_password@localhost:5432/tracker
DATABASE_ENCRYPTION_KEY=local_dev_key_123  # For field encryption

# Monitoring/Logging
LOG_LEVEL=debug
SENTRY_DSN=https://...  # Error tracking

# Security
SECRET_KEY=dev_secret_key_not_for_production
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

**File: .gitignore**
```
.env
.env.local
.env.*.local
secrets/
*.pem
*.key
.vscode/
__pycache__/
```

### Production Environment

**Docker Secrets Pattern**
```yaml
version: '3.9'

services:
  web:
    environment:
      DATABASE_URL: /run/secrets/database_url
      TWITTER_BEARER_TOKEN: /run/secrets/twitter_bearer_token
      SECRET_KEY: /run/secrets/secret_key

secrets:
  database_url:
    external: true     # Created by: echo "postgresql://..." | docker secret create database_url -
  twitter_bearer_token:
    external: true
  secret_key:
    external: true
```

**Alternative: HashiCorp Vault**
```python
from hvac import Client

vault = Client(url='https://vault.example.com:8200')
vault.auth.approle.login(role_id=role_id, secret_id=secret_id)

# Retrieve secrets
db_url = vault.secrets.kv.v2.read_secret_version(path='tracker/database_url')
twitter_token = vault.secrets.kv.v2.read_secret_version(path='tracker/twitter_bearer_token')
```

**Alternative: AWS Secrets Manager**
```python
import boto3

client = boto3.client('secretsmanager')

# Retrieve secret
response = client.get_secret_value(SecretId='tracker/database_url')
database_url = response['SecretString']

# Update secret (rotation)
client.update_secret(
    SecretId='tracker/twitter_bearer_token',
    SecretString=new_bearer_token
)
```

---

## 3. Config Class Pattern

### config.py
```python
import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class Config:
    """Base configuration"""
    
    # Flask
    FLASK_ENV: str = os.getenv('FLASK_ENV', 'development')
    DEBUG: bool = FLASK_ENV == 'development'
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # Database
    DATABASE_URL: str = os.getenv('DATABASE_URL', 
        'postgresql://track:tracker@localhost:5432/tracker'
    )
    DB_POOL_SIZE: int = int(os.getenv('DB_POOL_SIZE', 20))
    DB_POOL_RECYCLE: int = int(os.getenv('DB_POOL_RECYCLE', 3600))
    
    # Cache
    CACHE_ENABLED: bool = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
    CACHE_TTL: int = int(os.getenv('CACHE_TTL', 3600))
    REDIS_URL: Optional[str] = os.getenv('REDIS_URL')
    
    # API
    API_PORT: int = int(os.getenv('API_PORT', 5000))
    API_WORKERS: int = int(os.getenv('API_WORKERS', 4))
    API_TIMEOUT: int = int(os.getenv('API_TIMEOUT', 120))
    MAX_CONTENT_LENGTH: int = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'info')
    LOG_FORMAT: str = os.getenv('LOG_FORMAT', 'json')  # json or text
    
    # CORS
    CORS_ORIGINS: list = os.getenv('CORS_ORIGINS', 
        'http://localhost:3000,http://localhost:5000'
    ).split(',')
    
    # Platform credentials (loaded from secrets)
    TWITTER_BEARER_TOKEN: Optional[str] = os.getenv('TWITTER_BEARER_TOKEN')
    REDDIT_CLIENT_ID: Optional[str] = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET: Optional[str] = os.getenv('REDDIT_CLIENT_SECRET')
    MASTODON_TOKEN: Optional[str] = os.getenv('MASTODON_TOKEN')
    DISCORD_BOT_TOKEN: Optional[str] = os.getenv('DISCORD_BOT_TOKEN')
    LINKEDIN_BEARER_TOKEN: Optional[str] = os.getenv('LINKEDIN_BEARER_TOKEN')
    
    # Validation
    def validate(self):
        """Ensure critical config is present"""
        if self.FLASK_ENV == 'production':
            assert self.SECRET_KEY != 'dev-key-change-in-production', \
                "SECRET_KEY not set in production!"
            assert self.DATABASE_URL.startswith('postgresql://'), \
                "DATABASE_URL must be PostgreSQL in production"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'debug'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'info'
    
    def validate(self):
        super().validate()
        assert self.DEBUG is False, "DEBUG must be False in production"

class TestingConfig(Config):
    """Testing configuration"""
    FLASK_ENV = 'testing'
    TESTING = True
    DATABASE_URL = 'postgresql://localhost/tracker_test'
    LOG_LEVEL = 'warn'

# Select config based on environment
def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()
```

### Usage in Flask App
```python
from config import get_config

config = get_config()
config.validate()

app = Flask(__name__)
app.config.from_object(config)

# Database
db = SQLAlchemy(app)
db.engine.echo = config.DEBUG
```

---

## 4. Credential Encryption Strategy

### Data at Rest Encryption

**Option A: SQLAlchemy Hybrid Properties**
```python
from sqlalchemy_utils import EncryptedType
from cryptography.fernet import Fernet

class Credential(Base):
    __tablename__ = 'credentials'
    
    id = Column(UUID, primary_key=True)
    platform = Column(String)
    
    # Encrypted field using Fernet (symmetric encryption)
    encrypted_token = Column(
        EncryptedType(String, key='encryption_key'),
        nullable=False
    )
    
    @property
    def token(self):
        """Decrypt on read"""
        return decrypt_field(self.encrypted_token)
    
    @token.setter
    def token(self, value):
        """Encrypt on write"""
        self.encrypted_token = encrypt_field(value)
```

**Option B: Database Field-Level Encryption (pgcrypto)**
```sql
-- Create extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt on insert
INSERT INTO credentials(platform, encrypted_token)
VALUES('twitter', pgp_sym_encrypt('bearer_token_value', 'encryption_key'));

-- Decrypt on select
SELECT platform, pgp_sym_decrypt(encrypted_token, 'encryption_key') as token
FROM credentials;
```

**Option C: Application-Level Envelope Encryption**
```python
from cryptography.fernet import Fernet

class EncryptionManager:
    def __init__(self, master_key: str):
        self.cipher = Fernet(master_key.encode())
    
    def encrypt(self, plaintext: str) -> str:
        return self.cipher.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        return self.cipher.decrypt(ciphertext.encode()).decode()

# Usage
encryptor = EncryptionManager(os.getenv('ENCRYPTION_KEY'))
encrypted = encryptor.encrypt('bearer_token_123')
db.session.add(Credential(platform='twitter', encrypted_token=encrypted))

# Later
credential = db.session.query(Credential).filter_by(platform='twitter').first()
token = encryptor.decrypt(credential.encrypted_token)
```

---

## 5. Credentials API Endpoints

### User-Facing Endpoints

```python
# POST /api/credentials/add
# Add new credential for a platform
@app.route('/api/credentials/add', methods=['POST'])
def add_credential():
    """
    {
        "platform": "twitter",
        "type": "bearer_token",
        "value": "AAAABBBBCCCC...",
        "name": "prod"  # Optional identifier
    }
    """
    platform = request.json['platform']
    token = request.json['value']
    
    # Encrypt and store
    encrypted = encryptor.encrypt(token)
    cred = Credential(platform=platform, encrypted_token=encrypted)
    db.session.add(cred)
    db.session.commit()
    
    return {'status': 'stored', 'platform': platform}, 201

# GET /api/credentials/list
# List credentials (without values!)
@app.route('/api/credentials/list', methods=['GET'])
def list_credentials():
    """
    Returns [
        {
            "platform": "twitter",
            "type": "bearer_token",
            "added_at": "2026-04-18T...",
            "last_used": "2026-04-18T..."
        }
    ]
    """
    creds = db.session.query(Credential).all()
    return [{
        'platform': c.platform,
        'type': c.credential_type,
        'added_at': c.created_at.isoformat(),
        'last_used': c.last_used.isoformat() if c.last_used else None
    } for c in creds], 200

# DELETE /api/credentials/{platform}
# Delete credential
@app.route('/api/credentials/<platform>', methods=['DELETE'])
def delete_credential(platform):
    cred = db.session.query(Credential).filter_by(platform=platform).first()
    if cred:
        db.session.delete(cred)
        db.session.commit()
        return {'status': 'deleted'}, 200
    return {'error': 'not found'}, 404

# GET /api/credentials/test/{platform}
# Test if credential works
@app.route('/api/credentials/test/<platform>', methods=['GET'])
def test_credential(platform):
    cred = db.session.query(Credential).filter_by(platform=platform).first()
    if not cred:
        return {'error': 'credential not found'}, 404
    
    token = encryptor.decrypt(cred.encrypted_token)
    
    # Test (Twitter example)
    response = requests.get(
        'https://api.twitter.com/2/tweets/search/recent',
        headers={'Authorization': f'Bearer {token}'},
        params={'query': 'test', 'max_results': 10}
    )
    
    if response.ok:
        return {'status': 'valid'}, 200
    else:
        return {'status': 'invalid', 'error': response.text}, 400
```

---

## 6. Setup & Onboarding Workflow

### First-Time Setup (CLI)
```bash
./tracker setup

# Interactive prompts
> API endpoint: http://localhost:5000
> Add credentials? [y/n]: y
> Platform (twitter/reddit/mastodon/linkedin/discord/hackernews): twitter
> Token type (bearer_token/api_key/oauth2): bearer_token
> Paste bearer token (will be hidden): [hidden input]
> Another platform? [y/n]: n

✓ Configuration saved to ~/.tracker/config.toml
✓ Credentials encrypted and stored in database
```

### Docker Setup (.env)
```bash
docker run -e FLASK_ENV=production \
  -e DATABASE_URL=postgresql://tracker:password@db:5432/tracker \
  -e TWITTER_BEARER_TOKEN=${TWITTER_BEARER_TOKEN} \
  -e REDDIT_CLIENT_ID=${REDDIT_CLIENT_ID} \
  -e REDDIT_CLIENT_SECRET=${REDDIT_CLIENT_SECRET} \
  tracker-api:latest
```

### Kubernetes Setup (Secrets)
```bash
# Create secrets before deploying
kubectl create secret generic tracker-credentials \
  --from-literal=twitter-bearer-token=$(cat twitter_token.txt) \
  --from-literal=reddit-client-id=$(cat reddit_id.txt) \
  --from-literal=reddit-client-secret=$(cat reddit_secret.txt)

# Reference in deployment
env:
- name: TWITTER_BEARER_TOKEN
  valueFrom:
    secretKeyRef:
      name: tracker-credentials
      key: twitter-bearer-token
```

---

## 7. Environment-Specific Configurations

### Development (.env.dev)
```bash
FLASK_ENV=development
DEBUG=true
LOG_LEVEL=debug
DATABASE_URL=postgresql://tracker:tracker@localhost:5432/tracker
# Use mock credentials (no real API calls)
TWITTER_BEARER_TOKEN=mock_for_development
```

### Staging (.env.staging)
```bash
FLASK_ENV=staging
DEBUG=false
LOG_LEVEL=info
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@postgres-staging:5432/tracker
# Real credentials (test accounts)
TWITTER_BEARER_TOKEN=${STAGING_TWITTER_TOKEN}
```

### Production (.env.prod)
```bash
FLASK_ENV=production
DEBUG=false
LOG_LEVEL=warn
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@postgres-prod:5432/tracker
# Real credentials (production accounts)
TWITTER_BEARER_TOKEN=${PROD_TWITTER_TOKEN}
LOG_AGGREGATION_URL=https://logs.example.com
```

---

## 8. Credential Rotation Strategy

### Automated Rotation (Phase 5+)
```python
from schedule import every

# Every 90 days, remind to rotate credentials
@every(90).days
def remind_credential_rotation():
    creds = db.session.query(Credential).all()
    for cred in creds:
        days_old = (datetime.utcnow() - cred.created_at).days
        if days_old > 90:
            notification = Notification(
                type='credential_rotation_due',
                platform=cred.platform,
                days_old=days_old
            )
            db.session.add(notification)
    db.session.commit()

# Rotate on demand
def rotate_credential(platform: str, new_token: str):
    audit_log = AuditLog(
        event_type='credential_rotated',
        resource_type='credential',
        resource_id=platform,
        old_value={'token_hash': hash(old_token)},
        new_value={'token_hash': hash(new_token)},
        timestamp=datetime.utcnow()
    )
    db.session.add(audit_log)
    
    cred = db.session.query(Credential).filter_by(platform=platform).first()
    cred.encrypted_token = encryptor.encrypt(new_token)
    cred.last_rotated = datetime.utcnow()
    db.session.commit()
```

---

## 9. Implementation Checklist (Phase 4D)

**Files to Create**:
- [ ] `config.py` (Config class hierarchy)
- [ ] `.env.example` (template for .env file)
- [ ] `credential_manager.py` (encryption/decryption)
- [ ] `config_manager.py` (config file handling)
- [ ] `setup_credentials.py` (interactive onboarding)
- [ ] `CONFIG_GUIDE.md` (user documentation)

**Modifications to Existing Files**:
- [ ] `tracker_flask_api.py` → Load config from Config object
- [ ] `tracker_platform_adapters.py` → Get credentials from CredentialManager
- [ ] All modules → Use config.getattr() instead of hardcoded values
- [ ] `.gitignore` → Add .env, .env.local, secrets/

**Testing**:
- [ ] Test credential encryption/decryption
- [ ] Test .env file loading
- [ ] Test config precedence (env > file > default)
- [ ] Test credential API endpoints
- [ ] Test with mock vs. real credentials

**Deploy**:
- [ ] `git add [config files]`
- [ ] `git commit -m "PHASE 4D: Credentials & Configuration Management"`
- [ ] `git push origin main`

---

## 10. Success Criteria

✅ **Phase 4D Complete When**:
1. Config loads from multiple sources (env, file, secrets)
2. Credentials are encrypted in database
3. No credentials appear in logs or error messages
4. `POST /api/credentials/add` stores encrypted tokens
5. Scrapers retrieve credentials without decrypting in memory
6. `.env` file ignored by git
7. Setup wizard guides first-time users
8. Production config enforces secure defaults
9. Credential test endpoint (`GET /api/credentials/test/twitter`) validates tokens
10. All code pushed to GitHub with config guide

---

## 11. Security Checklist

- [ ] Never log sensitive data (patch logging)
- [ ] Credentials not in git history (`git clean -dfx .env`)
- [ ] Encryption key not in source code (from environment)
- [ ] HTTPS enforced in production (reverse proxy)
- [ ] Credentials cached in memory minimally
- [ ] HTTP basic auth not used (use bearer tokens)
- [ ] API keys rotated every 90 days
- [ ] All API calls use HTTPS (not HTTP)
- [ ] Credential audit log captures all access
- [ ] Database backups include encrypted values

---

## End Credentials & Configuration Architecture Document

**Next**: User review → Approval → Implementation of Phase 4D
