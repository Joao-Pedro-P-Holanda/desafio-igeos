from datetime import date, time

from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
)

# naming conventions make database migrations easier in multiple databases
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "pk_%(table_name)s",
}

commom_metadata = MetaData(naming_convention=convention)


class Base(MappedAsDataclass, DeclarativeBase):
    metadata = commom_metadata


class SubSystem(Base):
    __tablename__ = "subsistema"
    id_subsistema: Mapped[str] = mapped_column(primary_key=True)
    nome_subsistema: Mapped[str] = mapped_column()


class WeeklySubSystemMarginalCost(Base):
    __tablename__ = "custo_marginal_operacao_semanal"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_subsistema: Mapped[int] = mapped_column(ForeignKey("subsistema.id_subsistema"))

    custo_marginal_operacao_semanal: Mapped[float] = mapped_column()
    custo_marginal_operacao_semanal_carga_leve: Mapped[float] = mapped_column()
    custo_marginal_operacao_semanal_carga_media: Mapped[float] = mapped_column()
    custo_marginal_operacao_semanal_carga_pesada: Mapped[float] = mapped_column()

    data: Mapped[date] = mapped_column()


class HalfHourlySubSystemMarginalCost(Base):
    __tablename__ = "custo_marginal_operacao_semihorario"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_subsistema: Mapped[str] = mapped_column(ForeignKey("subsistema.id_subsistema"))

    custo_marginal_operacao: Mapped[float] = mapped_column()

    data: Mapped[date] = mapped_column()
    hora: Mapped[time] = mapped_column()


class PowerPlantVariableCost(Base):
    __tablename__ = "custo_variavel_unitario_usinas_termicas"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_subsistema: Mapped[str] = mapped_column(ForeignKey("subsistema.id_subsistema"))
    id_modelo_usina: Mapped[str] = mapped_column()
    usina: Mapped[str] = mapped_column()
    semana_operativa: Mapped[str] = mapped_column()
    custo_variavel_unitario: Mapped[float] = mapped_column()

    data_inicio: Mapped[date] = mapped_column()
    data_fim: Mapped[date] = mapped_column()


class SubSystemProductionStatement(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_subsistema: Mapped[str] = mapped_column(ForeignKey("subsistema.id_subsistema"))

    data: Mapped[date] = mapped_column()
    hora: Mapped[time] = mapped_column()

    geracao_eolica: Mapped[float | None] = mapped_column()
    geracao_termica: Mapped[float | None] = mapped_column()
    geracao_solar: Mapped[float | None] = mapped_column()
    geracao_hidraulica: Mapped[float | None] = mapped_column()


class HourlySubSystemProductionStatement(SubSystemProductionStatement):
    __tablename__ = "balanco_subsistema_horario"
    valor_carga: Mapped[float] = mapped_column()
    valor_intercambio: Mapped[float] = mapped_column()


class HalfHourlySubSystemProductionStatement(SubSystemProductionStatement):
    __tablename__ = "balanco_subsistema_semihorario"
    geracao_hidraulica_pequena_usina: Mapped[float] = mapped_column()
    geracao_termica_pequena_usina: Mapped[float] = mapped_column()
