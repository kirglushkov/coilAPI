from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
import uvicorn
from datetime import datetime
from database import SessionLocal, engine, CoilDB
from models import Coil, CoilStats
from sqlalchemy import and_, func

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.on_event("startup")
def startup():
    with SessionLocal() as session:
        session.execute("SELECT 1")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/coil", response_model=int)
async def create_coil(coil: Coil):
    with SessionLocal() as session:
        coil_data = CoilDB(**coil.model_dump(), created_at=datetime.now())
        session.add(coil_data)
        session.commit()
        session.refresh(coil_data)
        return coil_data.id

@app.delete("/api/coil/{id}")
async def delete_coil(id: int, db: Session = Depends(get_db)):
    with SessionLocal() as session:
        coil = session.query(CoilDB).filter(CoilDB.id == id).first()
        if not coil:
            raise HTTPException(status_code=404, detail="Coil not found")
        coil.deleted_at = datetime.now()
        session.commit()

# http://localhost:8000/api/coil/?start_id=0&end_id=10
@app.get("/api/coil")
async def get_coils(
    start_id: int = Query(default=None, description="Start ID for filtering"),
    end_id: int = Query(default=None, description="End ID for filtering"),
    start_weight: float = Query(default=None, description="Start weight for filtering"),
    end_weight: float = Query(default=None, description="End weight for filtering"),
    start_length: float = Query(default=None, description="Start length for filtering"),
    end_length: float = Query(default=None, description="End length for filtering"),
    start_added_date: datetime = Query(default=None, description="Start date of addition for filtering"),
    end_added_date: datetime = Query(default=None, description="End date of addition for filtering"),
    start_deleted_date: datetime = Query(default=None, description="Start date of deletion for filtering"),
    end_deleted_date: datetime = Query(default=None, description="End date of deletion for filtering"),
):
    with SessionLocal() as session:
        query = session.query(CoilDB)
        if start_id is not None:
            query = query.filter(CoilDB.id >= start_id)
        if end_id is not None:
            query = query.filter(CoilDB.id <= end_id)
        if start_weight is not None:
            query = query.filter(CoilDB.weight >= start_weight)
        if end_weight is not None:
            query = query.filter(CoilDB.weight <= end_weight)
        if start_length is not None:
            query = query.filter(CoilDB.length >= start_length)
        if end_length is not None:
            query = query.filter(CoilDB.length <= end_length)
        if start_added_date is not None:
            query = query.filter(CoilDB.created_at >= start_added_date)
        if end_added_date is not None:
            query = query.filter(CoilDB.created_at <= end_added_date)
        if start_deleted_date is not None:
            query = query.filter(CoilDB.deleted_at >= start_deleted_date)
        if end_deleted_date is not None:
            query = query.filter(CoilDB.deleted_at <= end_deleted_date)
        
        coils = query.all()
        
        return coils

@app.get("/api/coil/stats")
async def get_coil_stats(params: CoilStats):
    start_datetime = datetime.strptime(params.start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(params.end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

    with SessionLocal() as session:
        num_added_coils = session.query(CoilDB).filter(and_(CoilDB.created_at >= start_datetime, CoilDB.created_at <= end_datetime)).count()
        num_deleted_coils = session.query(CoilDB).filter(and_(CoilDB.deleted_at >= start_datetime, CoilDB.deleted_at <= end_datetime)).count()
        avg_length_weight = session.query(func.avg(CoilDB.length), func.avg(CoilDB.weight)).filter(and_(CoilDB.created_at >= start_datetime, CoilDB.created_at <= end_datetime)).first()
        max_min_length_weight = session.query(func.max(CoilDB.length), func.min(CoilDB.length), func.max(CoilDB.weight), func.min(CoilDB.weight)).filter(and_(CoilDB.created_at >= start_datetime, CoilDB.created_at <= end_datetime)).first()
        sum_weight = session.query(func.sum(CoilDB.weight)).filter(and_(CoilDB.created_at >= start_datetime, CoilDB.created_at <= end_datetime)).scalar()
        max_min_interval = session.query(func.max(CoilDB.deleted_at - CoilDB.created_at), func.min(CoilDB.deleted_at - CoilDB.created_at)).filter(and_(CoilDB.created_at >= start_datetime, CoilDB.created_at <= end_datetime)).first()

    return {
        "num_added_coils": num_added_coils,
        "num_deleted_coils": num_deleted_coils,
        "avg_length": avg_length_weight[0],
        "avg_weight": avg_length_weight[1],
        "max_length": max_min_length_weight[0],
        "min_length": max_min_length_weight[1],
        "max_weight": max_min_length_weight[2],
        "min_weight": max_min_length_weight[3],
        "sum_weight": sum_weight,
        "max_interval": max_min_interval[0],
        "min_interval": max_min_interval[1]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, workers=1, log_level='debug', access_log=True)