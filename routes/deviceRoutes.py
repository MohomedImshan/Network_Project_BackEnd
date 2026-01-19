from fastapi import APIRouter, Depends
from services.deviceServices import scan_network
from dependencies.auth import get_current_user

router = APIRouter()

@router.get("/getAllDevices")
def get_devices(current_user=Depends(get_current_user)):
    return {
        "count": len(scan_network()),
        "devices": scan_network()
    }