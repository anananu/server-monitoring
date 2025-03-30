from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing_extensions import Annotated

from models.model import Memory, System, Cpu, Core
import subprocess
import json 

from utils.script_runner import run_script
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session


app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

"""class MemorySchema(BaseModel):
    uuid: str
    hostname: str
    timestamp: str
    memory_total_mb: int
    memory_free_mb: int
    memory_available_mb: int
    swap_total_mb: int
    swap_free_mb: int
    page_faults: int
    page_reads: int
    page_writes: int
    pages_per_second: float
"""

@app.post("/sysinfo/", status_code=status.HTTP_201_CREATED)
async def get_sysinfo(db: db_dependency):
    sysinfo = run_script("./scripts/sys.sh")
    db_sysinfo = System(**sysinfo)

    db.add(db_sysinfo)
    db.commit()
    db.refresh(db_sysinfo)

    return {"status": "saved", "data": sysinfo}


@app.post("/memory/", status_code=status.HTTP_201_CREATED)
async def get_memory(db: db_dependency):
    memory_data = run_script("./scripts/memory.sh")
    #validated_data = MemorySchema(**memory_data)
    db_memory = Memory(**memory_data)

    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)

    return {"status": "saved", "data": memory_data}

@app.post("/cpu/", status_code=status.HTTP_201_CREATED)
async def get_cpu(db: db_dependency):
    cpu_data = run_script("./scripts/cpu.sh")
    db_cpu = Cpu(
        uuid = cpu_data["uuid"],
        hostname = cpu_data["hostname"],
        timestamp = cpu_data["timestamp"],
        model_name = cpu_data["model_name"],
        load_avg1 = cpu_data["load_avg1"],
        load_avg2 = cpu_data["load_avg2"],
        load_avg3 = cpu_data["load_avg3"],
    )

    db.add(db_cpu)
    db.commit()
    db.refresh(db_cpu)


    core_freqs = cpu_data["cpu_frequency"]
    for name, freq in core_freqs.items():
        db_core = Core(
            cpu_id = db_cpu.id, 
            name = name,
            freq = freq
        )
        db.add(db_core)
    db.commit()
    db.refresh(db_core)


    

    return {"status": "saved", "data": cpu_data}

@app.get("/")
def root():
    return{"Start"}

@app.get("/collect/{metric}")
async def collect(metric: str):
    allowed = {
        "cpu" : "./scripts/cpu.sh",
        "disk" : "./scripts/disk.sh",
        "memory" : "./scripts/memory.sh",
        "network" : "./scripts/network.sh",
        "proc" : "./scripts/proc.sh"
    }

    if metric not in allowed:
        raise HTTPException(status_code=404, detail="Metric not supported")
    
    data = run_script(allowed[metric])
    return JSONResponse(content=data)

