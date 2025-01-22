from datetime import datetime, timedelta
from dateutil import tz
from sys import stderr, stdin

class SnowflakeDiscord:
    def __init__(self, id: int):
        SnowflakeDiscord.__validate(id)
        
        self.id = id
        self.timestamp, self.machine_id, self.sequence = SnowflakeDiscord.__parse(id)
    
    def __str__(self):
        return "Snowflake: {{ " \
            f"id: {self.id}, " \
            f"timestamp: {self.timestamp}, " \
            f"machine_id: {self.machine_id}, " \
            f"sequence: {self.sequence}, " \
            f"creation_time: {self.creation_time} " \
        "}}"
    
    def creation_time_utc(self) -> datetime:
        EPOCH = datetime.strptime(
            "2015-1-1 00:00:00.000000",
            "%Y-%m-%d %H:%M:%S.%f"
        )
        ct = EPOCH + timedelta(milliseconds=self.timestamp)
        ct = ct.replace(tzinfo=tz.tzutc())
        return ct
    
    def creation_time_local(self) -> datetime:
        ct_utc = self.creation_time_utc()
        ct_local = ct_utc.astimezone(tz.tzlocal())
        return ct_local
    
    def description(self) -> str:
        ct = self.creation_time_local()
        day = ordinal(ct.day)
        moment_ms = datetime.strftime(ct, "%f")[:-3]
        moment = datetime.strftime(ct, f"%B {day}, %Y at %H:%M and %S.{moment_ms} seconds (%Z)")
        
        rank = ordinal(self.sequence + 1)
        
        return f"This user account was created at {moment}. " \
        f"The specific machine that generated its unique ID was identified with \"{self.machine_id}\". " \
        f"And within the millisecond that the ID was generated, it was {rank} in queue to be processed by that machine."
    
    @staticmethod
    def __validate(id: int):
        err_msg = f"\"{id}\" is not a valid Snowflake identifier: "

        if not isinstance(id, int):
            raise ValueError(err_msg + "not an integer.")
        if id < 0:
            raise ValueError(err_msg + "below accepted range.")
        if id > 0x7FFFFFFFFFFFFFFF:
            raise ValueError(err_msg + "above accepted range.")
    
    @staticmethod
    def __parse(id: int) -> tuple[datetime, int, int]:
        MASK_TIMESTAMP: int = 0xFFFFFFFFFFC00000
        MASK_MACHINE_ID: int = 0x3FF000
        MASK_SEQUENCE: int = 0xFFF
        
        timestamp = (MASK_TIMESTAMP & id) >> 22
        machine_id = (MASK_MACHINE_ID & id) >> 12
        sequence = MASK_SEQUENCE & id
        
        return timestamp, machine_id, sequence,

def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

def stderr_write(e: Exception):
    print(getattr(e, 'message', str(e)), file=stderr)

instructions = "Enter a Discord User ID, or \"q\" to exit."
print(instructions)

for query in stdin:
    query = query.rstrip()
    
    if (
        ("q" == query.lower()) or
        ("" == query)
    ):
        break
    
    try:
        query = int(query)
    except ValueError as e:
        stderr_write(ValueError(f"\"{query}\" is not a valid Snowflake identifier: not an integer."))
        continue
    
    try:
        id = SnowflakeDiscord(query)
        print(id.description())
    except ValueError as e:
        stderr_write(e)
        continue
        
    print(instructions)
