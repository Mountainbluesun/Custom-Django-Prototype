def current_user(request):
    # returns the JSON user stored in the session, or None
    return {"current_user": request.session.get("user")}