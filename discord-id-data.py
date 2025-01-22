from datetime import datetime, timedelta
from dateutil import tz
from sys import stderr, stdin

class SnowflakeDiscord:
    def __init__(self, id: int):
        SnowflakeDiscord.__validate(id)
        
        self.id = id
        self.timestamp, self.internal_worker_id, self.internal_process_id, self.sequence = SnowflakeDiscord.__parse(id)
    
    def __str__(self):
        return "Snowflake: {{ " \
            f"id: {self.id}, " \
            f"timestamp: {self.timestamp}, " \
            f"machine_id: {self.machine_id}, " \
            f"sequence: {self.sequence}, " \
        "}}"
    
    def description(self) -> str:
        day = ordinal(self.timestamp.day)
        moment_ms = datetime.strftime(self.timestamp, "%f")[:-3]
        moment = datetime.strftime(self.timestamp, f"%B {day}, %Y at %H:%M and %S.{moment_ms} seconds (%Z)")
        
        rank = ordinal(self.sequence + 1)
        
        return f"This user account was created at {moment}. " \
        f"The worker \"{self.internal_worker_id}\" and its process \"{self.internal_process_id}\" were involved in creating the ID. " \
        f"And within the millisecond of its generation, it was the {rank} in queue to be served by that process."
    
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
    def __parse(id: int) -> tuple[datetime, int, int, int]:
        EPOCH = datetime.fromtimestamp(1420070400).replace(tzinfo=tz.tzlocal())
        MASK_INTERNAL_WORKER_ID = 0x3E0000
        MASK_INTERNAL_PROCESS_ID = 0x1F000
        MASK_SEQUENCE = 0xFFF
        
        timestamp = EPOCH + timedelta(milliseconds=(id >> 22))
        internal_worker_id = (id & MASK_INTERNAL_WORKER_ID) >> 17
        internal_process_id = (id & MASK_INTERNAL_PROCESS_ID) >> 12
        sequence = id & MASK_SEQUENCE
        
        return timestamp, internal_worker_id, internal_process_id, sequence

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
