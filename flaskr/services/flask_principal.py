from flask_principal import Principal, Permission, RoleNeed, identity_loaded


principal_manager = Principal()

super_user = Permission(RoleNeed('super_user'))
user = Permission(RoleNeed('user'))
