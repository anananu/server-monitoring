from sqlalchemy import Boolean, Column, Float, BigInteger, SmallInteger, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class System(Base):
    __tablename__='systems'

    uuid = Column(String(32), primary_key=True, nullable=False)
    hostname = Column(String(253), nullable=False)
    os = Column(String(253), nullable=False)
    cpu = Column(String(253), nullable=False)

class Memory(Base):
    __tablename__ = 'memory'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(32), ForeignKey("systems.uuid", ondelete="CASCADE"), nullable=False)
    hostname = Column(String(253), nullable=False)
    timestamp = Column(String(25), nullable=False)
    memory_total_mb = Column(SmallInteger, nullable=False)
    memory_free_mb = Column(SmallInteger, nullable=False)
    memory_available_mb = Column(SmallInteger, nullable=False)
    swap_total_mb = Column(SmallInteger, nullable=False)
    swap_free_mb = Column(SmallInteger, nullable=False)
    page_faults = Column(BigInteger, nullable=False)
    page_reads = Column(BigInteger, nullable=False)
    page_writes = Column(BigInteger, nullable=False)
    pages_per_second = Column(Float, nullable=False)

class Cpu(Base):
    __tablename__ = 'cpu'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(32), ForeignKey("systems.uuid", ondelete="CASCADE"), index = True, nullable=False)
    hostname = Column(String(253), nullable=False)
    timestamp = Column(String(25), nullable=False)
    model_name = Column(String(253), nullable=False)
    load_avg1 = Column(Float, nullable = False)
    load_avg2 = Column(Float, nullable = False)
    load_avg3 = Column(Float, nullable = False)

    cores = relationship("Core", back_populates="cpu", passive_deletes=True, passive_updates=True)

class Core(Base):
    __tablename__ = 'cores'

    id = Column(SmallInteger, primary_key = True, autoincrement = True) 
    name = Column(String(32), nullable = False)
    cpu_id = Column(SmallInteger, ForeignKey("cpu.id", ondelete="CASCADE", onupdate="CASCADE"), index = True, nullable=False)
    freq = Column(Float, nullable = False)

    cpu = relationship("Cpu", back_populates="cores")

class Disk(Base):
    __tablename__ = 'disk'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(32), ForeignKey("systems.uuid", ondelete="CASCADE"), nullable=False)
    hostname = Column(String(253), nullable=False)
    timestamp = Column(String(25), nullable=False)
    disk_total = Column(String(6), nullable = False)
    disk_usage = Column(String(6), nullable = False)
    disk_free = Column(String(6), nullable = False)
    disk_reads = Column(String(32), nullable = False)
    disk_writes = Column(String(32), nullable = False)
    disk_queue_length = Column(BigInteger, nullable = False)
    nr_disk_partitions = Column(SmallInteger, nullable = False)

class Procces(Base):










