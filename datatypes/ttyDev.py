
class ttyDev(object):

   """
      ttydev=";auto;9600;N;8;1;"
   """
   def __init__(self, buff: str):
      self.buff: str = buff
      if self.buff[0] != self.buff[-1]:
         raise Exception(f"BadBuffString: {self.buff}")
      self.d = self.buff[0]
      arr: [] = self.buff.strip(self.d).split(self.d)
      self._dev, self._br, self._par, self._bits, self._sbits = arr

   @property
   def dev(self) -> str:
      return self._dev

   @property
   def baud(self) -> int:
      return int(self._br)

   @property
   def parity(self) -> str:
      return self._par

   def bits(self) -> int:
      return int(self._bits)

   @property
   def stop_bits(self) -> int:
      return int(self._sbits)
