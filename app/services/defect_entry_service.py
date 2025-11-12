from app.repositories.defect_entry_repo import DefectEntryRepository
from app.utils.db_connection import get_db
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    

class DefectEntryService:

    def add_defect(tv_seri_no: str, defect_catalog_id, found_by_pin: str,
                   status: str, line_id: int, catalog_id=None):
        
        db = next(get_db())

        if not tv_seri_no or not defect_catalog_id or not found_by_pin or not status:
            return {"message": "Zorunlu alanlar boş olamaz"}, 400
        
        if status not in ["REWORK", "HURDA"]:
            return {"message": "Geçersiz durum: sadece 'REWORK' veya 'HURDA' olabilir."}, 400

        # ✅ Tek hata mı? Çoklu mu? Tek ise liste yap
        if not isinstance(defect_catalog_id, list):
            defect_catalog_ids = [defect_catalog_id]
        else:
            defect_catalog_ids = defect_catalog_id

        # ✅ TV kontrol & oluşturma
        tv = DefectEntryRepository.get_tv_by_serial(db, tv_seri_no)
        if not tv:
            catalog = DefectEntryRepository.get_tv_catalog_by_barcode_prefix(db, tv_seri_no)
            if not catalog:
                return {"message": "TV Modeli bulunamadı"}, 404

            tv = DefectEntryRepository.create_tv(
                db=db,
                tv_seri_no=tv_seri_no,
                line_id=line_id,
                catalog_id=catalog.id
            )

        # ✅ Operatör kontrolü
        found_by = DefectEntryRepository.get_operator_by_pin(db, found_by_pin)
        if not found_by:
            return {"message": "Hatayı bulan operatör bulunamadı"}, 404

        created_defect_ids = []

        # ✅ Her hata için yeni defect kaydı oluştur
        for defect_id in defect_catalog_ids:
            defect = DefectEntryRepository.create_defect(
                db=db,
                tv_id=tv.id,
                defect_catalog_id=defect_id,
                found_by_id=found_by.id,
                status=status,
                line_id=line_id
            )

            created_defect_ids.append(defect.id)
            logger.info(f"Yeni hata kaydı oluşturuldu: {defect.id}")

        return {
            "message": "Hatalar başarıyla eklendi",
            "tv_serial": tv_seri_no,
            "found_by": f"{found_by.first_name} {found_by.last_name}",
            "defect_ids": created_defect_ids
        }, 201
