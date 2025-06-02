"""
This script handles user login and blockchain operations using FastAPI and SQLAlchemy.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import hashlib
import datetime
from typing import Optional
from pydantic import BaseModel
import jwt
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./blockchain.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# JWT Configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class Block(Base):
    __tablename__ = "blocks"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    data = Column(String)
    previous_hash = Column(String)
    hash = Column(String)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

class BlockchainManager:
    def __init__(self, db: Session):
        self.db = db
        self._ensure_genesis_block()
    
    def _ensure_genesis_block(self):
        if not self.db.query(Block).first():
            genesis = Block(
                data="Genesis Block",
                previous_hash="0",
                hash=self._calculate_hash("Genesis Block", "0")
            )
            self.db.add(genesis)
            self.db.commit()
    
    def _calculate_hash(self, data: str, previous_hash: str) -> str:
        content = f"{data}{previous_hash}{datetime.datetime.utcnow()}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def add_block(self, data: str):
        previous_block = self.db.query(Block).order_by(Block.id.desc()).first()
        new_block = Block(
            data=data,
            previous_hash=previous_block.hash,
            hash=self._calculate_hash(data, previous_block.hash)
        )
        self.db.add(new_block)
        self.db.commit()
        return new_block
    
    def validate_chain(self) -> bool:
        blocks = self.db.query(Block).order_by(Block.id).all()
        for i in range(1, len(blocks)):
            if blocks[i].previous_hash != blocks[i-1].hash:
                return False
        return True

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    token = jwt.encode(
        {"sub": user.username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    blockchain = BlockchainManager(db)
    blockchain.add_block(f"User {user.username} logged in")
    
    return {"access_token": token, "token_type": "bearer"}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head><title>Login</title></head>
        <body>
            <h1>Login</h1>
            <form action="/token" method="post">
                <input type="text" name="username" placeholder="Username"><br>
                <input type="password" name="password" placeholder="Password"><br>
                <button type="submit">Login</button>
            </form>
        </body>
    </html>
    """

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    blockchain = BlockchainManager(db)
    last_block = db.query(Block).order_by(Block.id.desc()).first()
    
    return f"""
    <html>
        <head><title>Dashboard</title></head>
        <body>
            <h1>Welcome {username}</h1>
            <p>Chain validation: {blockchain.validate_chain()}</p>
            <p>Last block hash: {last_block.hash}</p>
            <a href="/logout">Logout</a>
        </body>
    </html>
    """

@app.get("/logout")
async def logout():
    return {"message": "Logged out successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
