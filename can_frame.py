# Working on it

class CanFrame():
    def __init__(self, frame_id: int, extented_id_status: bool = True, fd_id_status: bool = True, payload_size: int = 1, payload: int = 1, delay: int = 0):
        self.frame_id = frame_id
        self.extented_id_status = extented_id_status
        self.fd_id_status = fd_id_status
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
        self.fd_id_status = new_fd_flag

    def get_fdflag(self):
        print(self.fd_id_status)
        return self.fd_id_status


    # ext id status
    def set_extflag(self, new_extented_id_status):
        self.extented_id_status = new_extented_id_status

    def get_extflag(self):
        print(self.extented_id_status)
        return self.extented_id_status

