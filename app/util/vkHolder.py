import vk


class VKHolder:
    session = vk.Session(access_token="394a2675e294ec4b83bc1b5d49607af45c6bd4d5aa8e3f55857baf40f579d2a82687ba542bf20125b51f9")
    api = vk.API(session,v=5.21)
    