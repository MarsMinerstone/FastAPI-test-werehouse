---
title: "FastAPI JWT MongoDB testing API"
date: 2022-05-24
draft: false
---

# How to use

### 1.

first of all **install** `requirements.txt`:

`pip install --user -r requirements.txt`

Some libraries might not be included in `requirements.txt`, sorry for that.

### 2.

Make shure you have **installed** MongoDB.

Create database in MongoDB.

Use `user.json` to **import** data to MongoDB database.

### 3. 

**Paste** name of your database to `config.py` for connection

### 4. 

Now you may **run** server using Web Server Uvicorn: `uvicorn main:app`

### 5. 

You can see user accounts in database for registration:

User with full access 
*username: mars* 
*password: secret* 
 
User with only read access: 
*username: Mark* 
*password: string* 