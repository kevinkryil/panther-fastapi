## Standard Definitions
- All  json values should return as 'detail':'value'
- Before every commit, update requirements.txt
- Before deleting validate if data exists all modules

## FOR MIGRATIONS 
- initial migration : alembic revision --autogenerate -m "Initial migration"
- new migration : alembic revision --autogenerate -m "Description of changes"
- apply migrations : alembic upgrade head
