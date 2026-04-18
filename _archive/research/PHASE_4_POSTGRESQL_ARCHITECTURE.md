# Phase 4C: PostgreSQL Persistence Architecture

**Status**: Design Phase (for review and approval)  
**Scope**: Database schema, migrations, ORM layer  
**Priority**: High (data durability) 

---

## 1. Current Data Model vs. Persistent Model

### Current State (Phase 3 - In-Memory)
```python
# All in memory, lost on server restart
jobs = {
    'job-123': {
        'id': 'job-123',
        'status': 'complete',
        'platforms': ['twitter', 'reddit'],
        'posts': [Post(...), Post(...)]
    }
}

# SQLite cache (temporary)
cache.get('twitter:query')  # 1-hour TTL
cache.set('twitter:query', data, ttl=3600)
```

**Limitations**:
- ❌ No persistence (restart loses all jobs)
- ❌ In-memory only scalability (RAM-bounded)
- ❌ No historical analytics
- ❌ No audit trail
- ❌ No concurrent access (single process only)

### Target State (Phase 4C - PostgreSQL)
```
Database Tables:
├── jobs (track all scraping operations)
├── posts (all scraped posts)
├── comments (all scraped comments)
├── analyses (analysis results + metrics)
├── elections (ZAP framework elections)
├── variations (pattern discoveries)
├── credentials (encrypted API keys)
└── audit_log (who did what when)

Benefits:
✅ Persistent across restarts
✅ Concurrent access (multi-process)
✅ Historical analytics (trends over time)
✅ Full audit trail
✅ Scalable to millions of records
✅ Backups & disaster recovery
```

---

## 2. Database Schema

### Table 1: jobs
```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Job metadata
    status VARCHAR(50) NOT NULL DEFAULT 'queued',  -- queued, scraping, analyzing, complete, error
    state_transitions JSONB NOT NULL DEFAULT '[]',  -- Track status history
    
    -- Configuration
    platforms TEXT[] NOT NULL,  -- Array of platform names
    search_query VARCHAR(1000) NOT NULL,
    limit_per_platform INTEGER DEFAULT 100,
    include_analysis BOOLEAN DEFAULT true,
    
    -- Progress
    progress_percent INTEGER DEFAULT 0,
    total_items INTEGER DEFAULT 0,
    completed_items INTEGER DEFAULT 0,
    
    -- Results
    total_posts INTEGER DEFAULT 0,
    total_comments INTEGER DEFAULT 0,
    total_elections INTEGER DEFAULT 0,
    
    -- User/context
    user_id VARCHAR(255),  -- For multi-user future
    api_version VARCHAR(10),
    
    -- Error handling
    error_message TEXT,
    error_stack_trace TEXT,
    
    -- Coherence
    coherence_score NUMERIC(3,2),
    coherence_metrics JSONB,
    
    -- Indexing
    INDEX idx_status(status),
    INDEX idx_created(created_at),
    INDEX idx_user(user_id),
    INDEX idx_platforms(platforms)
);
```

### Table 2: posts
```sql
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    
    -- Content
    platform VARCHAR(50) NOT NULL,
    platform_post_id VARCHAR(500) NOT NULL,  -- twitter:abc123, reddit:def456
    author_id VARCHAR(255),
    author_handle VARCHAR(255),
    text TEXT NOT NULL,
    
    -- Metadata
    created_at TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    engagement_count INTEGER DEFAULT 0,
    engagement_metrics JSONB,  -- {likes, retweets, shares, etc}
    
    -- Content classification
    language VARCHAR(5),
    sentiment VARCHAR(50),  -- positive, negative, neutral
    tags TEXT[],
    
    -- Relationships
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    INDEX idx_job_id(job_id),
    INDEX idx_platform(platform),
    INDEX idx_author(author_handle),
    INDEX idx_scraped(scraped_at)
);
```

### Table 3: comments
```sql
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    
    -- Content
    platform VARCHAR(50) NOT NULL,
    platform_comment_id VARCHAR(500),
    author_id VARCHAR(255),
    author_handle VARCHAR(255),
    text TEXT NOT NULL,
    
    -- Metadata
    created_at TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    engagement_count INTEGER DEFAULT 0,
    
    -- ZAP Analysis (computed during analysis)
    conflict_score NUMERIC(3,2),
    values_score NUMERIC(3,2),
    control_score NUMERIC(3,2),
    uncertainty_score NUMERIC(3,2),
    
    -- Indexing
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (post_id) REFERENCES posts(id),
    INDEX idx_job_id(job_id),
    INDEX idx_post_id(post_id),
    INDEX idx_platform(platform)
);
```

### Table 4: analyses
```sql
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL UNIQUE REFERENCES jobs(id) ON DELETE CASCADE,
    
    -- Timing
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analysis_duration_seconds NUMERIC,
    
    -- ZAP Framework Results
    conflicts_detected INTEGER,
    values_identified INTEGER,
    control_variations INTEGER,
    
    -- Coherence Metrics (4-part Φ proof)
    compression_ratio NUMERIC(4,3),  -- 0.0-1.0
    variation_coverage NUMERIC(4,3),
    prediction_accuracy NUMERIC(4,3),
    coherence_score NUMERIC(4,3),    -- Overall Φ
    
    -- Summary
    summary TEXT,
    top_themes JSONB,  -- [{theme, mention_count, confidence}]
    
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    INDEX idx_job_id(job_id),
    INDEX idx_coherence(coherence_score DESC)
);
```

### Table 5: elections
```sql
CREATE TABLE elections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    comment_id UUID REFERENCES comments(id) ON DELETE CASCADE,
    
    -- ZAP Election
    conflict VARCHAR(500),
    values_list TEXT[],
    control_statement VARCHAR(500),
    uncertainty_factors TEXT[],
    choices_available TEXT[],
    insight VARCHAR(1000),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confidence_score NUMERIC(3,2),
    
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    INDEX idx_job_id(job_id),
    INDEX idx_created(created_at)
);
```

### Table 6: variations
```sql
CREATE TABLE variations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    
    -- Pattern
    theme VARCHAR(500) NOT NULL,
    description TEXT,
    mention_count INTEGER,
    
    -- Members (elections/comments grouped by theme)
    election_ids UUID[] NOT NULL,
    comment_ids UUID[] NOT NULL,
    
    -- Coherence
    cluster_coherence NUMERIC(3,2),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    INDEX idx_job_id(job_id),
    INDEX idx_theme(theme)
);
```

### Table 7: credentials
```sql
CREATE TABLE credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Credential
    platform VARCHAR(50) NOT NULL,
    credential_type VARCHAR(50) NOT NULL,  -- bearertoken, api_key, oauth2, basic
    credential_name VARCHAR(255),  -- e.g., "twitter_prod", "reddit_test"
    
    -- Encrypted value (use pgcrypto or external envelope encryption)
    encrypted_value TEXT NOT NULL,
    encryption_key VARCHAR(255),  -- Reference to encryption key (not the key itself)
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_rotated TIMESTAMP,
    last_used TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    
    -- Audit
    created_by VARCHAR(255),
    rotated_by VARCHAR(255),
    
    CONSTRAINT unique_credential UNIQUE(platform, credential_type, credential_name),
    INDEX idx_platform(platform),
    INDEX idx_active(is_active)
);
```

### Table 8: audit_log
```sql
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Event
    event_type VARCHAR(100),  -- job_created, job_started, job_failed, scrape_started, etc
    resource_type VARCHAR(50),  -- job, post, comment, credential
    resource_id UUID,
    
    -- Changes
    old_value JSONB,
    new_value JSONB,
    change_summary VARCHAR(1000),
    
    -- User/Context
    user_id VARCHAR(255),
    ip_address INET,
    api_key_id UUID,
    
    -- Timing
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_event_type(event_type),
    INDEX idx_resource(resource_type, resource_id),
    INDEX idx_created(created_at)
);
```

---

## 3. ORM Layer (SQLAlchemy)

### Model Files

#### models/core.py
```python
from sqlalchemy import Column, String, Integer, Text, DateTime, JSONB, UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    status = Column(String(50), default='queued')
    platforms = Column(ARRAY(String))
    search_query = Column(String(1000), nullable=False)
    progress_percent = Column(Integer, default=0)
    
    # Relationships (lazy-loaded from comments)
    def to_dict(self):
        return {
            'id': str(self.id),
            'status': self.status,
            'platforms': self.platforms,
            'progress': self.progress_percent,
            'created_at': self.created_at.isoformat()
        }

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey('jobs.id'), nullable=False)
    
    platform = Column(String(50), nullable=False)
    platform_post_id = Column(String(500), nullable=False)
    author_handle = Column(String(255))
    text = Column(Text, nullable=False)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'platform': self.platform,
            'author': self.author_handle,
            'text': self.text,
            'created_at': self.created_at.isoformat()
        }

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey('jobs.id'), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey('posts.id'), nullable=False)
    
    platform = Column(String(50), nullable=False)
    text = Column(Text, nullable=False)
    author_handle = Column(String(255))
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'post_id': str(self.post_id),
            'platform': self.platform,
            'author': self.author_handle,
            'text': self.text
        }

# Similar for Analysis, Election, Variation, Credentials, AuditLog
```

### Database Session Management
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL', 
    'postgresql://tracker:password@localhost/tracker')

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=40)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for FastAPI/Flask routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
Base.metadata.create_all(bind=engine)
```

---

## 4. Migrations Strategy (Alembic)

### Initialize Migrations
```bash
alembic init alembic
```

### migration/env.py
```python
from alembic import context
from sqlalchemy import engine_from_config

def run_migrations_online():
    engine = engine_from_config(
        {'sqlalchemy.url': DATABASE_URL},
        poolclass=pool.NullPool
    )
    
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        
        with context.begin_transaction():
            context.run_migrations()
```

### Migration Workflow
```bash
# Create migration (auto-detect schema changes)
alembic revision --autogenerate -m "Add jobs table"

# Review migration file (alembic/versions/xxx.py)
# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### Version Control
```python
# In application
from alembic import __version__ as alembic_version

SCHEMA_VERSION = '1.0.0'  # Manually track major schema versions

# On startup, verify compatible:
if get_alembic_version() != SCHEMA_VERSION:
    raise RuntimeError("Database schema version mismatch")
```

---

## 5. Job Persistence Layer

### Job Repository Pattern
```python
class JobRepository:
    def __init__(self, db_session):
        self.db = db_session
    
    def create_job(self, platforms: list, query: str, limit: int) -> str:
        """Create new job and return ID"""
        job = Job(
            platforms=platforms,
            search_query=query,
            limit_per_platform=limit,
            status='queued'
        )
        self.db.add(job)
        self.db.commit()
        return str(job.id)
    
    def get_job(self, job_id: str) -> Job:
        """Get job by ID"""
        return self.db.query(Job).filter(Job.id == job_id).first()
    
    def update_job_status(self, job_id: str, status: str, progress: int = None):
        """Update job status"""
        job = self.get_job(job_id)
        job.status = status
        if progress is not None:
            job.progress_percent = progress
        job.updated_at = datetime.utcnow()
        
        # Track state transitions
        job.state_transitions.append({
            'from': job.status,
            'to': status,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        self.db.commit()
    
    def list_jobs(self, limit: int = 10, user_id: str = None) -> list:
        """List recent jobs"""
        query = self.db.query(Job).order_by(Job.created_at.desc())
        if user_id:
            query = query.filter(Job.user_id == user_id)
        return query.limit(limit).all()
    
    def delete_old_jobs(self, days: int = 30):
        """Clean up old jobs"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        self.db.query(Job).filter(Job.created_at < cutoff_date).delete()
        self.db.commit()
```

### Post/Comment Persistence
```python
class PostRepository:
    def batch_insert_posts(self, job_id: str, posts: list[Post]):
        """Insert scraped posts in batch"""
        db_posts = [
            Post(
                job_id=job_id,
                platform=post.platform,
                platform_post_id=post.platform_id,
                author_handle=post.author,
                text=post.content,
                engagement_metrics=post.metrics.to_dict()
            )
            for post in posts
        ]
        self.db.bulk_insert_mappings(Post, db_posts)
        self.db.commit()
        return [str(p.id) for p in db_posts]

class CommentRepository:
    def batch_insert_comments(self, job_id: str, comments: list[Comment]):
        """Insert comments with ZAP scores"""
        db_comments = [
            Comment(
                job_id=job_id,
                post_id=comment.post_id,
                platform=comment.platform,
                text=comment.text,
                author_handle=comment.author,
                conflict_score=comment.zap.conflict_score,
                values_score=comment.zap.values_score,
                # ... other ZAP scores
            )
            for comment in comments
        ]
        self.db.bulk_insert_mappings(Comment, db_comments)
        self.db.commit()
```

---

## 6. Query Optimization

### Indexes (Already in Schema)
```
posts(job_id, platform)  -- Query by job + platform
comments(job_id, post_id)  -- Nested queries
jobs(status, created_at)  -- Status filtering, recent jobs
```

### Connection Pooling
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,          # Default: 5
    max_overflow=40,       # Allow 40 more connections
    pool_recycle=3600,     # Recycle after 1 hour (PostgreSQL timeout)
    pool_pre_ping=True     # Test connections before use
)
```

### Query Patterns
```python
# ❌ SLOW: Load all jobs with all posts
jobs = db.query(Job).all()  # N+1 problem
for job in jobs:
    posts = job.posts  # Queries DB for each job

# ✅ FAST: Use joinedload
jobs = db.query(Job).options(
    joinedload(Job.posts)
).all()

# ✅ Another option: Select only needed columns
jobs = db.query(
    Job.id, 
    Job.status, 
    func.count(Post.id).label('post_count')
).outerjoin(Post).group_by(Job.id).all()
```

---

## 7. Data Migration Strategy

### From In-Memory to PostgreSQL

**Phase 4C Task**:
1. Create PostgreSQL database
2. Migrate Phase 3 data (if needed):
   - Export current in-memory jobs to JSON
   - Write migration script to import into PostgreSQL
3. Update Flask API to use PostgreSQL instead of in-memory
4. Verify data integrity

**Migration Script**:
```python
def migrate_from_memory_to_db(memory_jobs: dict):
    """Migrate data from Phase 3 in-memory to PostgreSQL"""
    from models import Job, Post, Comment
    
    for job_id, job_data in memory_jobs.items():
        db_job = Job(
            id=job_id,
            status=job_data['status'],
            platforms=job_data['platforms'],
            search_query=job_data['query']
        )
        db.add(db_job)
        
        for post in job_data.get('posts', []):
            db_post = Post(
                job_id=job_id,
                platform=post.platform,
                text=post.content
            )
            db.add(db_post)
    
    db.commit()
```

---

## 8. Backup & Disaster Recovery

### Automated Backups
```bash
# Daily backup script
#!/bin/bash
pg_dump -h postgres -U tracker tracker > /backups/tracker_$(date +%Y%m%d).sql

# Weekly compressed
pg_dump -h postgres -U tracker tracker | gzip > /backups/tracker_$(date +%Y%m%d).sql.gz

# Keep 30 days
find /backups -name "tracker_*.sql.gz" -mtime +30 -delete
```

### Kubernetes Backup (Phase 5+)
```yaml
# VolumeSnapshot for PostgreSQL persistent volume
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: tracker-db-backup
spec:
  volumeSnapshotClassName: csi-snapshotter
  source:
    persistentVolumeClaimName: postgres-pvc
```

---

## 9. Implementation Checklist (Phase 4C)

**Database Setup**:
- [ ] Create PostgreSQL database (`tracker`)
- [ ] Create user (`tracker`) with password
- [ ] Test connection from app

**ORM & Models**:
- [ ] Create `models/__init__.py`
- [ ] Create `models/core.py` (8 SQLAlchemy models)
- [ ] Create `models/repositories.py` (CRUD classes)
- [ ] Create database session manager file

**Migrations**:
- [ ] Initialize Alembic
- [ ] Create initial schema migration
- [ ] Test migration on clean database

**API Updates**:
- [ ] Modify `tracker_flask_api.py` to use SQLAlchemy
- [ ] Replace in-memory job queue with DB queries
- [ ] Update all endpoints to use repositories
- [ ] Add transaction management

**Testing**:
- [ ] Test job creation → database insert
- [ ] Test job retrieval → database query
- [ ] Test post/comment persistence
- [ ] Test analysis storage
- [ ] Verify data survives server restart

**Deploy**:
- [ ] `git add [model files, migrations]`
- [ ] `git commit -m "PHASE 4C: PostgreSQL Persistence Layer"`
- [ ] `git push origin main`

---

## 10. Success Criteria

✅ **Phase 4C Complete When**:
1. PostgreSQL database contains all 8 tables with correct schema
2. Flask API successfully creates jobs in database
3. Jobs persist across server restarts
4. All queries return correct data (SELECT verify)
5. Relationships work (job → posts → comments)
6. Analysis results stored in analyses table
7. Audit log captures all operations
8. All code pushed to GitHub with migration files
9. Server can handle 100+ concurrent jobs
10. Data integrity check passes (`pg_dump | md5sum` consistent)

---

## 11. Performance Targets

| Operation | Target | Current |
|-----------|--------|---------|
| Create job | < 100ms | ✓ |
| List jobs (10 items) | < 50ms | ? |
| Get job details | < 100ms | ? |
| Insert 100 posts | < 500ms | ? |
| Query by platform | < 100ms | ? |
| Backup (1M records) | < 30s | N/A |

---

## End PostgreSQL Architecture Document

**Next**: User review → Approval → Implementation of Phase 4C
