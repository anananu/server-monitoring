from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing_extensions import Annotated, Dict, List

from models.model import Memory, System, Cpu, Core, Disk, Network, Interface, Procces
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

class SysSchema(BaseModel):
    uuid: str
    hostname: str
    os: str
    cpu: str

class MemorySchema(BaseModel):
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

class CpuSchema(BaseModel):
    uuid: str
    hostname: str
    timestamp: str
    model_name: str
    load_avg1: float
    load_avg2: float 
    load_avg3: float
    cpu_frequency: Dict[str, float]

class ProcessDetailSchema(BaseModel):
    user: str
    pid: int
    cpu: float
    mem: float
    stat: str
    start: str
    time: str
    command: str

class ProcSchema(BaseModel):
    uuid: str
    hostname: str
    timestamp: str
    top_processes: List[ProcessDetailSchema]

class DiskSchema(BaseModel):
    uuid: str
    hostname: str
    timestamp: str
    disk_total_GB: float
    disk_usage_GB: float
    disk_free_GB: float
    disk_reads_sectors: int 
    disk_writes_sectors: int
    disk_queue_length: int
    nr_disk_partitions: int

class InterfaceSchema(BaseModel):
    interface: str
    connectivity: str
    availability: str
    ipv4_address: str
    ipv6_address: str
    throughput_rx_KBs: float
    throughput_tx_KBs: float

class NetworkSchema(BaseModel):
    uuid: str
    hostname: str
    timestamp: str
    interfaces: List[InterfaceSchema]

@app.post("/sysinfo/", status_code=status.HTTP_201_CREATED)
async def get_sysinfo(sysinfo: SysSchema, db: db_dependency):
    db_sysinfo = db.query(System).filter(System.uuid == sysinfo.uuid).first()
    if db_sysinfo:
        db_sysinfo.hostname = sysinfo.hostname
        db_sysinfo.os = sysinfo.os
        db_sysinfo.cpu_model = sysinfo.cpu
    else:
        db_sysinfo = System(**sysinfo.model_dump())
        db.add(db_sysinfo)
    
    db.commit()
    db.refresh(db_sysinfo)
    return {"status": "saved", "data": sysinfo.model_dump()}


@app.post("/memory/", status_code=status.HTTP_201_CREATED)
async def get_memory(memory: MemorySchema, db: db_dependency):
    db_memory = db.query(Memory)
    db_memory = Memory(**memory.model_dump())
    
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)

    return {"status": "saved", "data": memory.model_dump()}

@app.post("/cpu/", status_code=status.HTTP_201_CREATED)
async def get_cpu(cpu_data: CpuSchema, db: db_dependency):
    db_cpu = Cpu(
        uuid=cpu_data.uuid,
        hostname=cpu_data.hostname,
        timestamp=cpu_data.timestamp,
        model_name=cpu_data.model_name,
        load_avg1=cpu_data.load_avg1,
        load_avg2=cpu_data.load_avg2,
        load_avg3=cpu_data.load_avg3
    )
    db.add(db_cpu)
    db.commit()
    db.refresh(db_cpu) 

    for core_name, freq in cpu_data.cpu_frequency.items():
        db_core = Core(
            cpu_id=db_cpu.id,  
            name=core_name,
            freq=freq
        )
        db.add(db_core)
    db.commit()
    db.refresh(db_core)

    return {"status": "saved", "data": cpu_data.model_dump()}

@app.post("/disk/", status_code=status.HTTP_201_CREATED)
async def get_disk(disk: DiskSchema, db: db_dependency):
    disk_data=db.query(Disk)
    db_disk = Disk(**disk.model_dump())

    db.add(db_disk)
    db.commit()
    db.refresh(db_disk)

    return {"status": "saved", "data": disk.model_dump()}

@app.post("/proc/", status_code=status.HTTP_201_CREATED)
async def get_proc(proc_data: ProcSchema, db: db_dependency):
    for proc in proc_data.top_processes:
        db_proc = Procces(
            uuid = proc_data.uuid,
            hostname = proc_data.hostname,
            timestamp = proc_data.timestamp,
            user = proc.user,
            pid = proc.pid,
            cpu = proc.cpu,
            mem = proc.mem,
            stat = proc.stat,
            start = proc.start,
            time = proc.time,
            command = proc.command
        )
        db.add(db_proc)
    
    db.commit()
    db.refresh(db_proc)

    return {"status": "saved", "data": proc_data.model_dump()}

@app.post("/network/", status_code=status.HTTP_201_CREATED)
async def get_network(network: NetworkSchema, db: db_dependency):
    db_network = Network(
        uuid=network.uuid,
        hostname=network.hostname,
        timestamp=network.timestamp
    )
    db.add(db_network)
    db.commit()
    db.refresh(db_network)
    
    for detail in network.interfaces:
        db_interface = Interface(
            reg_id=db_network.id,
            interface=detail.interface,
            connectivity=detail.connectivity,
            availability=detail.availability,
            ipv4_address=detail.ipv4_address,
            ipv6_address=detail.ipv6_address,
            throughput_rx_KBs=detail.throughput_rx_KBs,
            throughput_tx_KBs=detail.throughput_tx_KBs,
        )
        db.add(db_interface)
    
    db.commit()
    db.refresh(db_interface)
    return {"status": "saved", "data": network.model_dump()}


    
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

