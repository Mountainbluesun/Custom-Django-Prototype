# src/core/context.py
def current_user(request):
    return {"current_user": request.session.get("user")}
