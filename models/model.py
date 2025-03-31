from sqlalchemy import Boolean, Column, Float, BigInteger, SmallInteger, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class System(Base):
    __tablename__='systems'

    uuid = Column(String(32), primary_key=True, nullable=False)
    hostname = Column(String(253), nullable=False)
    os = Column(String(253), nullable=False)
    cpu = Column(String(253), nullable=False)

    memory = relationship("Memory", back_populates="systems", passive_deletes=True)
    disk = relationship("Disk", back_populates="systems", passive_deletes=True)
    network = relationship("Network", back_populates="systems", passive_deletes=True)
    processes = relationship("Procces", back_populates="systems", passive_deletes=True)
    cpus = relationship("Cpu", back_populates="systems", passive_deletes=True)


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

    systems = relationship("System", back_populates="memory")

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

    systems = relationship("System", back_populates="cpus")
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
    disk_total_GB = Column(SmallInteger, nullable = False)
    disk_usage_GB = Column(SmallInteger, nullable = False)
    disk_free_GB = Column(SmallInteger, nullable = False)
    disk_reads_sectors = Column(Integer, nullable = False)
    disk_writes_sectors = Column(Integer, nullable = False)
    disk_queue_length = Column(BigInteger, nullable = False)
    nr_disk_partitions = Column(SmallInteger, nullable = False)

    systems = relationship("System", back_populates="disk")

class Procces(Base):
    __tablename__ = 'processes'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(32), ForeignKey("systems.uuid", ondelete="CASCADE"), nullable=False)
    hostname = Column(String(253), nullable=False)
    timestamp = Column(String(25), nullable=False)
    user = Column(String(253), nullable=False)
    pid = Column(Integer, nullable=False)
    cpu = Column(Float, nullable=False)
    mem = Column(Float, nullable=False)
    stat = Column(String(255), nullable=False)
    start = Column(String(255), nullable=False)
    time = Column(String(255), nullable=False)
    command = Column(String(255), nullable=False)

    systems = relationship("System", back_populates="processes")

class Network(Base):
    __tablename__ = 'network'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(32), ForeignKey("systems.uuid", ondelete="CASCADE"), nullable=False)
    hostname = Column(String(253), nullable=False)
    timestamp = Column(String(25), nullable=False)

    interfaces = relationship("Interface", back_populates="network", passive_deletes=True, passive_updates=True)
    systems = relationship("System", back_populates="network")

class Interface(Base):
    __tablename__ = 'interfaces'

    id = Column(SmallInteger, primary_key = True, autoincrement = True)
    reg_id = Column(SmallInteger, ForeignKey("network.id", ondelete="CASCADE"), nullable=False)
    interface = Column(String(255), nullable=False)
    connectivity = Column(String(32), nullable=False)
    availability = Column(String(32), nullable=False)
    ipv4_address = Column(String(15), nullable=False)
    ipv6_address = Column(String(32), nullable=False)
    throughput_rx_KBs = Column(Float, nullable=False)
    throughput_tx_KBs = Column(Float, nullable=False)

    network = relationship("Network", back_populates="interfaces")













