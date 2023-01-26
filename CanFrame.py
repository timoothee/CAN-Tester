# Working on it

class Can():
    def __init__(self, frame_id: int, ext_flag: bool = True, fd_flag: int = 100, payload_size: int = 1, payload: int = 1, delay: int = 0):
        self.frame_id = frame_id
        self.ext_flag = ext_flag
        self.fd_flag = fd_flag
        self.payload_size = payload_size
        self.payload = payload
        self.delay = delay

    # id
    def set_id(self, new_id):
        self.frame_id = new_id

    def get_id(self):
        print(self.frame_id)
        return self.frame_id

    # fd flag
    def set_fd_flag(self, new_fd_flag):
        self.fd_flag = new_fd_flag

    def get_fdflag(self):
        print(self.fd_flag)
        return self.fd_flag


    # ext flag
    def set_extflag(self, new_flag):
        self.ext_flag = new_flag

    def get_extflag(self):
        print(self.ext_flag)
        return self.ext_flag

