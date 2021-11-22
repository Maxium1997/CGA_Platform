from django.contrib.auth.decorators import login_required


# Function's permission authorize user to use that function
def permission_check(required_privilege):
    def decorator(view):
        @login_required
        def check(request, *args, **kwargs):
            if not required_privilege:
                raise ValueError("Loss argument 'required_privilege'")

            if not request.user.has_perm(required_privilege):
                raise PermissionError

            return view(request, *args, **kwargs)
        return check
    return decorator
