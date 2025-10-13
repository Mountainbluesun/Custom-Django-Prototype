def current_user(request):
    # renvoie l’utilisateur JSON stocké en session, ou None
    return {"current_user": request.session.get("user")}
