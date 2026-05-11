# -*- coding: utf-8 -*-
from datetime import datetime, UTC
import time
import ntplib

class TimeClient:
    def __init__(self):
        self.ntp_offset = 0
        self.is_synced = False
            
    def syncTime(self):    
        try:
            c = ntplib.NTPClient()
            response = c.request('europe.pool.ntp.org', version=3)
            self.ntp_offset = response.tx_time - time.time()
            self.is_synced = True
            print("NTP synced")            
        except Exception as e:
            self.is_synced = False
            print(f"NTP failed: {e}")
    
    def getEpochTime(self, unit="ms"):    
        epoch_time_s = time.time() + self.ntp_offset        
        if unit=="s":
            return epoch_time_s
        elif unit=='ms':
            return int(epoch_time_s*1e3)
        elif unit=='ns':
            return int(epoch_time_s*1e9)        
        else:
            print(f"unit {unit} not supported")
            return None
    
    def getIsoFormat(self):
        t = self.getEpochTime(unit='s')
        return datetime.fromtimestamp(t, UTC).isoformat()        
    
    def getFormattedDate(self, fmt='%Y%m%dT%H:%M:%S'):
        t = self.getEpochTime(unit='s')
        return datetime.fromtimestamp(t, UTC).strftime(fmt)