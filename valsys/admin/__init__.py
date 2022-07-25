def login():
    """Login into the valsys system.
    
    Stores credentials locally in order to be used
    during API authentication."""
    from valsys.admin.service import _login_cli
    _login_cli()
