import enum

import pydantic as pydantic_v2

from pcapi import settings
from pcapi.connectors.big_query.queries.base import BaseQuery


class ClosedVenueStatusEnum(enum.Enum):
    A = "A"
    F = "F"


class ClosedVenueSirenModel(pydantic_v2.BaseModel):
    venue_id: int
    status: ClosedVenueStatusEnum


class ClosedVenuesSirenQuery(BaseQuery):
    raw_query = f"""
        select
            venue_id,
            etatAdministratifUniteLegale as status,
        from
            -- TODO: table name might not the right
            `{settings.BIG_QUERY_CLEANED_TABLE_BASENAME}.siret_data`
        where
            DATE(dateDernierTraitementEtablissement) >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY)
    """

    model = ClosedVenueSirenModel
