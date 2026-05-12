# -*- coding: utf-8 -*-
from datetime import datetime, UTC
import time
import ntplib

class NTPTimeClient:
    def __init__(self):
        self.ntp_offset = 0
        self.is_synced = False
            
    def sync_ntp(self):    
        try:
            client = ntplib.NTPClient()
            response = client.request('europe.pool.ntp.org', version=3, timeout=5)
            self.ntp_offset = response.offset
            self.is_synced = True
            print(f"NTP synced. Offset: {self.ntp_offset:.3f} s")
        except Exception as e:
            self.is_synced = False
            print(f"NTP failed: {e}")
    
    def get_epoch_time(self, unit="s"):            
        t_s = time.time() + self.ntp_offset
        if unit=="s":
            return t_s
        elif unit=='ms':
            return int(t_s*1e3)
        elif unit=='ns':
            # Warning: npt offset only valid for millisecond precision
            # For nanosecond precision use time.time_ns()
            return int(t_s*1e9)
        else:
            raise ValueError(f"Invalid unit '{unit}'. Supported units are 's', 'ms', 'ns'.")            
    
    def get_isoformat(self):
        t = self.get_epoch_time(unit='s')
        return datetime.fromtimestamp(t, UTC).isoformat().replace('+00:00', 'Z')
    
    def get_formatted_date(self, fmt='%Y%m%dT%H:%M:%S'):
        t = self.get_epoch_time(unit='s')
        return datetime.fromtimestamp(t, UTC).strftime(fmt)