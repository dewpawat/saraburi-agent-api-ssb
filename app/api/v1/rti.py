from fastapi import APIRouter, Request, Depends, params, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import settings

from app.api.v1.models.rti_model import (
    RTIAccidentRequest, RTIAccidentPlaceRequest,
    RTIAccidentResponse, RTIAccidentPlaceResponse,
)
from app.api.v1.deps.header import get_header_security
from app.api.v1.models.security_model import HeaderSecurity
from app.core.security import api_security
from app.core.database import get_db

router = APIRouter()

@router.post(
    "/accident",
    summary="RTI Accident",
    description="ข้อมูลการเกิดอุบัติเหตุ",
    response_model=RTIAccidentResponse,
    status_code=status.HTTP_200_OK,
)
async def rti_accident(
    body: RTIAccidentRequest,
    request: Request,
    headers: HeaderSecurity = Depends(get_header_security),
    db: AsyncSession = Depends(get_db),
):
    await api_security(request, body.hospcode)

    params = {
        "vstdate": body.vstdate
    }

    sql = text("""
        SELECT 
            * FROM v_rti_accident 
        WHERE vstdate = :vstdate 
        ORDER BY DATETIME_SERV DESC
    """
    )
    rows = await db.execute(sql, params)
    result = rows.mappings().all()
    if not result:
        return {
            "MessageCode": "404",
            "Message": "Not Found Data",
            "result": []
        }

    list_data = []
    for row in result:
        temp = {
            "HOSPCODE": str(row["HOSPCODE"]),
            "PID": str(row["PID"]),
            "SEQ": str(row["SEQ"]),
            "DATETIME_SERV": str(row["DATETIME_SERV"]),
            "DATETIME_AE": str(row["DATETIME_AE"]) if row["DATETIME_AE"] else None,
            "AETYPE": str(row["AETYPE"]) if row["AETYPE"] else None,
            "AEPLACE": str(row["AEPLACE"]) if row["AEPLACE"] else None,
            "TYPEIN_AE": str(row["TYPEIN_AE"]) if row["TYPEIN_AE"] else None,
            "TRAFFIC": str(row["TRAFFIC"]) if row["TRAFFIC"] else None,
            "VEHICLE": str(row["VEHICLE"]) if row["VEHICLE"] else None,
            "ALCOHOL": str(row["ALCOHOL"]) if row["ALCOHOL"] else None,
            "NACROTIC_DRUG": str(row["NACROTIC_DRUG"]) if row["NACROTIC_DRUG"] else None,
            "BELT": str(row["BELT"]) if row["BELT"] else None,
            "HELMET": str(row["HELMET"]) if row["HELMET"] else None,
            "AIRWAY": str(row["AIRWAY"]) if row["AIRWAY"] else None
            ,"STOPBLEED": str(row["STOPBLEED"]) if row["STOPBLEED"] else None,
            "SPLINT": str(row["SPLINT"]) if row["SPLINT"] else None,
            "FLUID": str(row["FLUID"]) if row["FLUID"] else None,
            "URGENCY": str(row["URGENCY"]) if row["URGENCY"] else None,
            "COMA_EYE": str(row["COMA_EYE"]) if row["COMA_EYE"] else None,
            "COMA_SPEAK": str(row["COMA_SPEAK"]) if row["COMA_SPEAK"] else None,
            "COMA_MOVEMENT": str(row["COMA_MOVEMENT"]) if row["COMA_MOVEMENT"] else None,
            "D_UPDATE": str(row["D_UPDATE"]) if row["D_UPDATE"] else None,
            "CID": str(row["CID"]) if row["CID"] else None,
            "HOSPCODE9": str(row["HOSPCODE9"]) if row["HOSPCODE9"] else None,
            "accident_stdcode": str(row["accident_stdcode"]) if row["accident_stdcode"] else None,
            "pt_name": str(row["pt_name"]) if row["pt_name"] else None,
            "hn": str(row["hn"]) if row["hn"] else None,
            "an": str(row["an"]) if row["an"] else None,
            "referhos": str(row["referhos"]) if row["referhos"] else None,
            "dead_in": str(row["dead_in"]) if row["dead_in"] else None,
            "dead_before": str(row["dead_before"]) if row["dead_before"] else None,
            "place_other": str(row["place_other"]) if row["place_other"] else None,
        }
        list_data.append(temp)

    return {
        "MessageCode": "200",
        "Message": "Success",
        "result": list_data
    }

@router.post(
    "/place",
    summary="RTI AccidentPlace",
    description="ข้อมูลจุดเสี่ยง",
    response_model=RTIAccidentPlaceResponse,
    status_code=status.HTTP_200_OK,
)
async def rti_place(
    body: RTIAccidentPlaceRequest,
    request: Request,
    headers: HeaderSecurity = Depends(get_header_security),
    db: AsyncSession = Depends(get_db),
):
    await api_security(request, body.hospcode)

    sql = text("""
        SELECT * FROM v_rti_place ORDER BY accident_stdcode ASC
    """)

    rows = await db.execute(sql)
    result = rows.mappings().all()

    if not result:
        return {
            "MessageCode": "404",
            "Message": "Not Found Data",
            "result": []
        }

    list_data = []
    for row in result:
        temp = {
            "accident_stdcode": str(row["accident_stdcode"]),
            "accident_place_type_name": str(row["accident_place_type_name"]),
            "latitude": str(row["latitude"]),
            "longitude": str(row["longitude"]),
            "tamboncode": str(row["tamboncode"]),
            "ampurcode": str(row["ampurcode"]),
            "road": str(row["road"]),
            "export_code": str(row["export_code"]),
        }
        list_data.append(temp)

    return {
        "MessageCode": "200",
        "Message": "Success",
        "result": list_data
    }