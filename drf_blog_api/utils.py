import uuid
from django.conf import settings

def upload( file, upload_dir="" ):
    info = {
        "success" : False,
        "msg" : "Something went wrong",
        "path" : None
    }

    try:
        if file:
            extension = file.name.split(".")[-1]
            file_name = f"{uuid.uuid4()}.{extension}"
            upload_path = f"{settings.ABS_UPLOAD_DIR}{file_name}"
            destination_file = open( upload_path, '+wb' )
            
            with destination_file as destination:
                info["path"] = file_name
                info["success"] = True
                info["msg"] = "Successful"
                for chunk in file.chunks():
                    destination.write(chunk)
    except Exception as ex:
        info["msg"] = str(ex)

    return info