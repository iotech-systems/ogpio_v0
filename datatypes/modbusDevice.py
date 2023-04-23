
import typing as _t
from datatypes.modbusGPIO import modbusGPIO
from datatypes.ttyDev import ttyDev


class modbusDevice(object):

    def __init__(self, devid: str, comm: str, mb_adr: int, lbl: str):
        self.devid: str = devid
        self.comm: str = comm
        self.mb_adr: int = mb_adr
        self.lbl: str = lbl
        self.GPIOS: _t.List[modbusGPIO] = []
        self.ttydev: ttyDev = ttyDev(self.comm)

    def __str__(self):
        buff: str = "".join([f"\t{str(g)}\n" for g in self.GPIOS])
        return f"[ devid: {self.devid} | comm: {self.comm} |" \
            f" mb_adr: {self.mb_adr} | lbl: {self.lbl} ]\n{buff}"
