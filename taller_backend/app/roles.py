from fastapi import Depends, HTTPException, status
from .auth_utils import get_current_active_user
from . import models

def require_role(*roles_permitidos: str):
    """
    Devuelve una dependencia que valida que el usuario tenga uno de los roles permitidos.
    Ejemplo:
        @app.get("/admin", dependencies=[Depends(require_role("admin"))])
    """
    def role_checker(
        usuario: models.Usuario = Depends(get_current_active_user)
    ):
        rol_usuario = usuario.rol.nombre.lower()

        if rol_usuario not in [r.lower() for r in roles_permitidos]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere rol: {roles_permitidos}"
            )

        return usuario

    return role_checker
