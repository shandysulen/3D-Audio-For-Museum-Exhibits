import socket
import crcmod
from time import sleep
from time import perf_counter
import struct

class BeaconUDP:
    _payload_offset = 5
    _request_header = bytearray(b'\x47\x01\x00\x04\x00\x00\x10')

    def __init__(self, ip, port, beacon_id):
        self.ip = ip
        self.port = port
        self.beacon_id = beacon_id
        self._request_header = beacon_id.to_bytes(1, byteorder='little') + self._request_header

        crc16 = crcmod.predefined.Crc('modbus')
        crc16.update(self._request_header)

        # generate packet CRC
        # seems like correct CRC is not necessary for request packet
        self.request_packet = self._request_header + crc16.digest()

        # create UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.udp_socket.bind((self.ip, 49100))
        # print("Source socket binded to port:",49100)
        try:
            self.udp_socket.connect((self.ip, self.port))
            print("Connection estabished!")
        except socket.timeout:
            print('Connection timeout, check IP address and port number of the target server')
        except OSError:
            print('\nCannot build connection to the Server/Dashboard')

    def __del__(self):
        if self.udp_socket is not None:
            self.udp_socket.close()

    def close(self):
        self.udp_socket.close()

    def request_position(self):
        self.udp_socket.send(self.request_packet)

        data, address = self.udp_socket.recvfrom(1024)

        # parse the packet, '<' for little endian; 'L' for unsigned long(4);
        # 'h' for short integer(2); 'B' for unsigned char(1); 'x' for pad byte(1); 'H' for unsigned short(2)
        # details of String Format: https://docs.python.org/3.5/library/struct.html
        timestamp, coord_x, coord_y, coord_z, data_crc16 = struct.unpack_from('<LhhhxxxxxxH',
                                                                              data, self._payload_offset)
        print(coord_x,coord_y,coord_z)
        return (coord_x,coord_y,coord_z)

def udp_factory(ip, port, beacon_add):
    udp = BeaconUDP(ip, port, beacon_add)
    return udp
