from datetime import date
from fastapi import APIRouter, Security
from ..core.security import validate_token


router = APIRouter(dependencies=[Security(validate_token)])




