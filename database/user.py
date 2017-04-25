
# Import 'class database' for connection with database


# class User(object):
#     def __init__(self):
#         self.users = {}
#
#     def find_by_id(self):
#         pass
#
#     def get_users(self):
#         return self.users


users = {
    "a3235dec-58a8-4716-90f5-6df2423ffb54": {
        "name": "andrew",
        "password": "123",
        "email": "email@gmail.com",
        "md5_hash": "202cb962ac59075b964b07152d234b70"
    },

    "f965d4cf-1256-4b3d-93dd-e3f7ecfa08f9": {
        "name": "test",
        "password": "1234",
        "email": "email@gmail.com",
        "md5_hash": "81dc9bdb52d04dc20036dbd8313ed055"
    },

    "a2598c98-1f62-4a6b-815d-03497522a7a3": {
        "name": "admin",
        "password": "admin",
        "email": "email@gmail.com",
        "md5_hash": ""
    },

    "c1002399-a3b0-4fe8-8b68-597977c03e97": {
        "name": "user",
        "password": "user",
        "email": "email@gmail.com",
        "md5_hash": ""
    }
}


blacklisted_tokens = []
